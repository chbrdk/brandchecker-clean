#!/usr/bin/env python3
"""
BrandChecker File Upload Service
Sichere Datei-Upload API für PDF und Bilddateien
"""

import os
import uuid
import magic
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import PyPDF2
from PIL import Image, UnidentifiedImageError
import fitz  # PyMuPDF
import base64
from io import BytesIO
from pdf2image import convert_from_path

app = Flask(__name__)

# CORS aktivieren für Frontend-Zugriff
CORS(app, origins=[
    "http://localhost:8005",  # Frontend App
    "http://localhost:3001",  # Vite Dev Server
    "http://brandchecker-app:3001",  # Docker Internal
    "*"  # Temporär für Development
], supports_credentials=True)

# Konfiguration
UPLOAD_FOLDER = '/shared/uploads'
PREVIEW_FOLDER = '/shared/previews'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
PREVIEW_SIZE = (300, 300)  # Thumbnail-Größe
ALLOWED_EXTENSIONS = {
    'pdf': ['application/pdf'],
    'images': [
        'image/jpeg',
        'image/jpg', 
        'image/png',
        'image/gif',
        'image/bmp',
        'image/tiff',
        'image/webp'
    ]
}

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Stelle sicher, dass Upload- und Preview-Ordner existieren
Path(UPLOAD_FOLDER).mkdir(parents=True, exist_ok=True)
Path(PREVIEW_FOLDER).mkdir(parents=True, exist_ok=True)

class FileValidator:
    """Validiert hochgeladene Dateien auf Sicherheit und Echtheit"""
    
    @staticmethod
    def get_mime_type(file_path: str) -> str:
        """Ermittelt den MIME-Type einer Datei"""
        try:
            return magic.from_file(file_path, mime=True)
        except Exception:
            return 'application/octet-stream'
    
    @staticmethod
    def validate_pdf(file_path: str) -> Dict[str, Any]:
        """Validiert PDF-Dateien"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                
                # Basis-Validierung
                if len(reader.pages) == 0:
                    return {'valid': False, 'error': 'PDF hat keine Seiten'}
                
                # Metadaten extrahieren
                metadata = reader.metadata or {}
                
                return {
                    'valid': True,
                    'pages': len(reader.pages),
                    'encrypted': reader.is_encrypted,
                    'metadata': {
                        'title': metadata.get('/Title', ''),
                        'author': metadata.get('/Author', ''),
                        'creator': metadata.get('/Creator', ''),
                        'producer': metadata.get('/Producer', ''),
                        'creation_date': str(metadata.get('/CreationDate', '')),
                        'modification_date': str(metadata.get('/ModDate', ''))
                    }
                }
        except Exception as e:
            return {'valid': False, 'error': f'PDF-Validierung fehlgeschlagen: {str(e)}'}
    
    @staticmethod
    def validate_image(file_path: str) -> Dict[str, Any]:
        """Validiert Bilddateien"""
        try:
            with Image.open(file_path) as img:
                # Basis-Validierung
                if img.size[0] == 0 or img.size[1] == 0:
                    return {'valid': False, 'error': 'Bild hat ungültige Dimensionen'}
                
                # Versuche das Bild zu laden (erkennt korrupte Dateien)
                img.load()
                
                return {
                    'valid': True,
                    'dimensions': img.size,
                    'mode': img.mode,
                    'format': img.format,
                    'has_transparency': img.mode in ('RGBA', 'LA') or 'transparency' in img.info
                }
        except UnidentifiedImageError:
            return {'valid': False, 'error': 'Datei ist kein gültiges Bild'}
        except Exception as e:
            return {'valid': False, 'error': f'Bild-Validierung fehlgeschlagen: {str(e)}'}

class PreviewGenerator:
    """Generiert Preview-Bilder für verschiedene Dateitypen"""
    
    @staticmethod
    def generate_pdf_preview(file_path: str, preview_path: str) -> Dict[str, Any]:
        """Generiert Preview-Bild von der ersten PDF-Seite"""
        try:
            # Verwende pdf2image für robuste PDF-Verarbeitung
            images = convert_from_path(file_path, first_page=1, last_page=1, dpi=150)
            
            if not images:
                return {'success': False, 'error': 'PDF hat keine Seiten'}
            
            # Erste Seite als Bild
            img = images[0]
            original_size = img.size
            
            # Thumbnail erstellen
            img.thumbnail(PREVIEW_SIZE, Image.Resampling.LANCZOS)
            
            # Als PNG speichern
            img.save(preview_path, "PNG", optimize=True)
            
            return {
                'success': True,
                'preview_path': preview_path,
                'dimensions': img.size,
                'original_dimensions': original_size,
                'pages_total': len(images)
            }
            
        except Exception as e:
            return {'success': False, 'error': f'PDF-Preview fehlgeschlagen: {str(e)}'}
    
    @staticmethod
    def generate_image_preview(file_path: str, preview_path: str) -> Dict[str, Any]:
        """Generiert Preview-Thumbnail von Bilddateien"""
        try:
            with Image.open(file_path) as img:
                # Konvertiere zu RGB falls nötig (für JPEG-Kompatibilität)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Erstelle weißen Hintergrund für Transparenz
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Original-Dimensionen speichern
                original_size = img.size
                
                # Thumbnail erstellen
                img.thumbnail(PREVIEW_SIZE, Image.Resampling.LANCZOS)
                
                # Als JPEG speichern (kleinere Dateigröße)
                img.save(preview_path, "JPEG", quality=85, optimize=True)
                
                return {
                    'success': True,
                    'preview_path': preview_path,
                    'dimensions': img.size,
                    'original_dimensions': original_size
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Bild-Preview fehlgeschlagen: {str(e)}'}
    
    @staticmethod
    def image_to_base64(image_path: str) -> str:
        """Konvertiert Bild zu Base64 für direkten Browser-Transfer"""
        try:
            with open(image_path, 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                
                # Bestimme MIME-Type basierend auf Dateiendung
                ext = Path(image_path).suffix.lower()
                mime_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
                
                return f"data:{mime_type};base64,{img_base64}"
        except Exception:
            return ""

def get_file_hash(file_path: str) -> str:
    """Berechnet SHA-256 Hash einer Datei"""
    hash_sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def is_allowed_file(filename: str, mime_type: str) -> bool:
    """Prüft ob Datei erlaubt ist basierend auf Extension und MIME-Type"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    # Prüfe PDF
    if extension == 'pdf':
        return mime_type in ALLOWED_EXTENSIONS['pdf']
    
    # Prüfe Bilder
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp']
    if extension in image_extensions:
        return mime_type in ALLOWED_EXTENSIONS['images']
    
    return False

@app.route('/health', methods=['GET'])
def health_check():
    """Gesundheitscheck für den Service"""
    return jsonify({
        'status': 'healthy',
        'service': 'file-upload',
        'timestamp': datetime.utcnow().isoformat(),
        'upload_folder': UPLOAD_FOLDER,
        'max_file_size_mb': MAX_FILE_SIZE // (1024 * 1024)
    })

@app.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    """
    Hauptendpoint für Datei-Upload
    
    Returns:
        JSON mit Dateiinformationen oder Fehlermeldung
    """
    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        # Prüfe ob Datei in Request vorhanden
        if 'file' not in request.files:
            return jsonify({'error': 'Keine Datei im Request gefunden'}), 400
        
        file = request.files['file']
        
        # Prüfe ob Datei ausgewählt wurde
        if file.filename == '':
            return jsonify({'error': 'Keine Datei ausgewählt'}), 400
        
        # Sichere Dateinamen
        original_filename = file.filename
        secure_name = secure_filename(original_filename)
        
        if not secure_name:
            return jsonify({'error': 'Ungültiger Dateiname'}), 400
        
        # Generiere eindeutige ID und Pfad
        file_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        filename_with_id = f"{timestamp}_{file_id}_{secure_name}"
        file_path = os.path.join(UPLOAD_FOLDER, filename_with_id)
        
        # Speichere Datei temporär
        file.save(file_path)
        
        # Validiere Datei
        mime_type = FileValidator.get_mime_type(file_path)
        file_size = os.path.getsize(file_path)
        
        # Prüfe erlaubte Dateitypen
        if not is_allowed_file(secure_name, mime_type):
            os.remove(file_path)  # Lösche ungültige Datei
            return jsonify({
                'error': 'Dateityp nicht erlaubt',
                'detected_mime_type': mime_type,
                'allowed_types': ALLOWED_EXTENSIONS
            }), 400
        
        # Validiere je nach Dateityp
        validation_result = None
        file_type = 'unknown'
        
        print(f"🔍 Erkannter MIME-Type: {mime_type}")
        
        if mime_type in ALLOWED_EXTENSIONS['pdf']:
            file_type = 'pdf'
            print(f"📄 Validiere PDF: {original_filename}")
            validation_result = FileValidator.validate_pdf(file_path)
        elif mime_type in ALLOWED_EXTENSIONS['images']:
            file_type = 'image'
            print(f"🖼️ Validiere Bild: {original_filename}")
            validation_result = FileValidator.validate_image(file_path)
        
        print(f"✅ Dateityp bestimmt: {file_type}")
        
        # Prüfe Validierungsergebnis
        if validation_result and not validation_result['valid']:
            os.remove(file_path)  # Lösche ungültige Datei
            return jsonify({
                'error': 'Datei-Validierung fehlgeschlagen',
                'details': validation_result['error']
            }), 400
        
        # Berechne Datei-Hash
        file_hash = get_file_hash(file_path)
        
        print(f"🔍 Starte Preview-Generierung für {file_type}: {original_filename}")
        
        # Generiere Preview
        preview_filename = f"preview_{file_id}.{'png' if file_type == 'pdf' else 'jpg'}"
        preview_path = os.path.join(PREVIEW_FOLDER, preview_filename)
        preview_result = None
        preview_base64 = None
        
        try:
            if file_type == 'pdf':
                print(f"🖼️ Generiere PDF-Preview für: {original_filename}")
                preview_result = PreviewGenerator.generate_pdf_preview(file_path, preview_path)
            elif file_type == 'image':
                print(f"🖼️ Generiere Bild-Preview für: {original_filename}")
                preview_result = PreviewGenerator.generate_image_preview(file_path, preview_path)
            
            # Konvertiere Preview zu Base64 wenn erfolgreich
            if preview_result and preview_result['success']:
                print(f"✅ Preview erfolgreich generiert: {preview_path}")
                preview_base64 = PreviewGenerator.image_to_base64(preview_path)
                print(f"📦 Base64 generiert: {len(preview_base64)} Zeichen")
            else:
                print(f"❌ Preview-Generierung fehlgeschlagen: {preview_result}")
        except Exception as e:
            print(f"❌ Fehler bei Preview-Generierung: {str(e)}")
            preview_result = {'success': False, 'error': str(e)}
        
        # Erfolgreiche Upload-Antwort
        response_data = {
            'success': True,
            'file_id': file_id,
            'original_filename': original_filename,
            'stored_filename': filename_with_id,
            'file_path': file_path,
            'relative_path': f'/shared/uploads/{filename_with_id}',
            'file_type': file_type,
            'mime_type': mime_type,
            'file_size_bytes': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'file_hash_sha256': file_hash,
            'upload_timestamp': datetime.utcnow().isoformat(),
            'validation': validation_result,
            'preview': {
                'available': preview_result['success'] if preview_result else False,
                'path': preview_path if preview_result and preview_result['success'] else None,
                'base64': preview_base64,
                'dimensions': preview_result.get('dimensions') if preview_result and preview_result['success'] else None
            }
        }
        
        # Logge erfolgreichen Upload
        print(f"✅ Datei erfolgreich hochgeladen: {filename_with_id} ({file_type}, {file_size} bytes)")
        
        return jsonify(response_data), 200
        
    except RequestEntityTooLarge:
        return jsonify({
            'error': 'Datei zu groß',
            'max_size_mb': MAX_FILE_SIZE // (1024 * 1024)
        }), 413
    except Exception as e:
        # Cleanup bei Fehler
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        print(f"❌ Upload-Fehler: {str(e)}")
        return jsonify({'error': f'Upload fehlgeschlagen: {str(e)}'}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """Listet alle hochgeladenen Dateien auf"""
    try:
        files = []
        upload_path = Path(UPLOAD_FOLDER)
        
        for file_path in upload_path.glob('*'):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'filename': file_path.name,
                    'path': str(file_path),
                    'size_bytes': stat.st_size,
                    'size_mb': round(stat.st_size / (1024 * 1024), 2),
                    'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    'mime_type': FileValidator.get_mime_type(str(file_path))
                })
        
        return jsonify({
            'files': sorted(files, key=lambda x: x['modified'], reverse=True),
            'total_files': len(files),
            'upload_folder': UPLOAD_FOLDER
        })
    except Exception as e:
        return jsonify({'error': f'Fehler beim Auflisten: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({
        'error': 'Datei zu groß',
        'max_size_mb': MAX_FILE_SIZE // (1024 * 1024)
    }), 413

if __name__ == '__main__':
    print("🚀 BrandChecker File Upload Service startet...")
    print(f"📁 Upload-Ordner: {UPLOAD_FOLDER}")
    print(f"📏 Max. Dateigröße: {MAX_FILE_SIZE // (1024 * 1024)}MB")
    print(f"📋 Erlaubte Dateitypen: PDF, Bilder")
    
    app.run(host='0.0.0.0', port=8006, debug=True)
