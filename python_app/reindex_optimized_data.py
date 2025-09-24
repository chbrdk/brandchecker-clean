#!/usr/bin/env python3
"""
Master-Script für optimierte Daten-Indexierung:
1. Optimiert Brand-Daten
2. Importiert in Datenbank
3. Generiert Embeddings
4. Optimiert Indizes
"""

import os
import sys
import subprocess
import logging
from typing import List

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OptimizedReindexer:
    def __init__(self):
        self.scripts_dir = "python_app"
        self.scripts = [
            "optimize_brand_data.py",
            "import_optimized_data.py", 
            "embedding_service.py",
            "optimize_indexes.py"
        ]
    
    def run_script(self, script_name: str, description: str) -> bool:
        """Führt ein Python-Script aus"""
        logger.info(f"🚀 Starte: {description}")
        
        script_path = os.path.join(self.scripts_dir, script_name)
        
        if not os.path.exists(script_path):
            logger.error(f"❌ Script nicht gefunden: {script_path}")
            return False
        
        try:
            # Führe Script aus
            result = subprocess.run([
                sys.executable, script_path
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                logger.info(f"✅ Erfolgreich: {description}")
                if result.stdout:
                    logger.info(f"Output: {result.stdout}")
                return True
            else:
                logger.error(f"❌ Fehler bei: {description}")
                logger.error(f"Error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Ausführungsfehler bei {description}: {e}")
            return False
    
    def check_prerequisites(self) -> bool:
        """Prüft Voraussetzungen"""
        logger.info("🔍 Prüfe Voraussetzungen...")
        
        # Prüfe ob Docker läuft
        try:
            result = subprocess.run([
                "docker", "compose", "ps"
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode != 0:
                logger.error("❌ Docker Compose nicht verfügbar")
                return False
            
            # Prüfe ob Services laufen
            if "brandchecker-postgres" not in result.stdout:
                logger.error("❌ PostgreSQL Service nicht verfügbar")
                return False
            
            if "brandchecker-llm-api" not in result.stdout:
                logger.error("❌ LLM API Service nicht verfügbar")
                return False
            
            logger.info("✅ Alle Services laufen")
            return True
            
        except Exception as e:
            logger.error(f"❌ Fehler bei Docker-Prüfung: {e}")
            return False
    
    def run_optimized_reindex(self) -> bool:
        """Führt optimierte Neu-Indexierung durch"""
        logger.info("🎯 Starte optimierte Neu-Indexierung...")
        
        # Prüfe Voraussetzungen
        if not self.check_prerequisites():
            return False
        
        # Schritt 1: Optimiere Daten
        if not self.run_script(
            "optimize_brand_data.py",
            "Optimierung der Brand-Daten (Duplikate entfernen, Farben extrahieren)"
        ):
            return False
        
        # Schritt 2: Importiere optimierte Daten
        if not self.run_script(
            "import_optimized_data.py", 
            "Import der optimierten Daten in PostgreSQL"
        ):
            return False
        
        # Schritt 3: Generiere Embeddings
        if not self.run_script(
            "embedding_service.py",
            "Generierung der Embeddings für semantische Suche"
        ):
            return False
        
        # Schritt 4: Optimiere Indizes
        if not self.run_script(
            "optimize_indexes.py",
            "Optimierung der Vektor-Indizes für bessere Performance"
        ):
            return False
        
        logger.info("🎉 Optimierte Neu-Indexierung erfolgreich abgeschlossen!")
        return True
    
    def show_statistics(self):
        """Zeigt Statistiken der optimierten Daten"""
        logger.info("📊 Statistiken der optimierten Daten:")
        
        try:
            # Lade Optimierungs-Statistiken
            stats_file = "shared/JSON/optimized/optimization_stats.json"
            if os.path.exists(stats_file):
                import json
                with open(stats_file, 'r', encoding='utf-8') as f:
                    stats = json.load(f)
                
                html_stats = stats.get('html_optimization', {})
                graphql_stats = stats.get('graphql_optimization', {})
                
                logger.info(f"📄 HTML-Optimierung:")
                logger.info(f"   - Einträge: {html_stats.get('original_entries', 0)}")
                logger.info(f"   - Farben gefunden: {html_stats.get('colors_found', 0)}")
                logger.info(f"   - Duplikate entfernt: {html_stats.get('duplicates_removed', 0)}")
                logger.info(f"   - Einträge gesplittet: {html_stats.get('entries_split', 0)}")
                
                logger.info(f"🗂️ GraphQL-Optimierung:")
                logger.info(f"   - Brands: {graphql_stats.get('brands', 0)}")
                logger.info(f"   - Assets: {graphql_stats.get('assets', 0)}")
                logger.info(f"   - Duplikate entfernt: {graphql_stats.get('duplicates_removed', 0)}")
                
            else:
                logger.info("📊 Statistiken nicht verfügbar")
                
        except Exception as e:
            logger.error(f"❌ Fehler beim Laden der Statistiken: {e}")

def main():
    """Hauptfunktion"""
    logger.info("🚀 Starte optimierte Brand-Daten-Indexierung...")
    
    reindexer = OptimizedReindexer()
    
    # Führe optimierte Neu-Indexierung durch
    success = reindexer.run_optimized_reindex()
    
    if success:
        # Zeige Statistiken
        reindexer.show_statistics()
        
        logger.info("🎯 Nächste Schritte:")
        logger.info("   1. Teste die API: python_app/test_llm_system.py")
        logger.info("   2. Prüfe n8n Workflow mit optimierten Daten")
        logger.info("   3. Die semantische Suche sollte jetzt viel schneller sein!")
        
    else:
        logger.error("❌ Optimierte Neu-Indexierung fehlgeschlagen!")
        logger.info("💡 Tipps:")
        logger.info("   1. Prüfe ob alle Docker Services laufen")
        logger.info("   2. Prüfe die Logs der einzelnen Scripts")
        logger.info("   3. Stelle sicher, dass die Datenbank erreichbar ist")
        
        sys.exit(1)

if __name__ == "__main__":
    main()
