# Storybook Setup Dokumentation

## Übersicht
Das BrandChecker-Projekt verwendet Storybook für die Entwicklung und Dokumentation von React-Komponenten. Storybook läuft in einem Docker-Container und ist über Port 8004 erreichbar.

## Zugriff
- **URL:** http://localhost:8004
- **Port:** 8004 (extern) → 6006 (intern)
- **Container:** brandchecker-storybook

## Technische Details

### Dockerfile.storybook
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build-storybook
EXPOSE 6006
CMD ["npm", "run", "storybook", "--", "--no-open"]
```

### Wichtige Konfigurationen
- **Node.js Version:** 20 (erforderlich für Storybook 9.1.8)
- **Build-Prozess:** Statische Dateien werden vor Container-Start gebaut
- **Browser-Öffnen:** Deaktiviert (`--no-open`) für Docker-Kompatibilität
- **Port-Mapping:** 127.0.0.1:8004 → Container:6006

### Docker Compose Integration
```yaml
brandchecker-storybook:
  build: 
    context: ./frontend
    dockerfile: Dockerfile.storybook
  container_name: brandchecker-storybook
  restart: unless-stopped
  ports:
    - "127.0.0.1:8004:6006"
  environment:
    - NODE_ENV=development
  volumes:
    - ./frontend/src:/app/src:ro
    - ./frontend/.storybook:/app/.storybook:ro
  networks:
    - brandchecker_network
```

## Entwicklungsworkflow

### Storybook starten
```bash
cd /Users/m4mini/Desktop/DOCKER-local/brandchecker
docker-compose up -d --build brandchecker-storybook
```

### Logs überprüfen
```bash
docker-compose logs brandchecker-storybook
```

### Status überprüfen
```bash
docker-compose ps brandchecker-storybook
```

## Troubleshooting

### Problem: Container crasht mit xdg-open Fehler
**Lösung:** `--no-open` Parameter im Dockerfile hinzufügen

### Problem: Node.js Version zu alt
**Lösung:** Node.js 20+ verwenden (aktuell: node:20-alpine)

### Problem: Port nicht erreichbar
**Lösung:** 
1. Container-Status prüfen: `docker-compose ps`
2. Logs prüfen: `docker-compose logs brandchecker-storybook`
3. Port-Mapping überprüfen: 8004 → 6006

## Nächste Schritte
- Komponenten-Architektur definieren
- Grundlegende UI-Komponenten implementieren
- Storybook-Stories für alle Komponenten erstellen
- Design System etablieren
