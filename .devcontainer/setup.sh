#!/bin/bash

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt
pip install -r sidecar-requirements.txt
pip install -r ui-requirements.txt

echo "[*] Building Docker images..."
docker build . -f alpespartners.Dockerfile -t alpespartners/flask
docker build . -f adaptador.Dockerfile -t alpespartners/adaptador
docker build . -f notificacion.Dockerfile -t alpespartners/notificacion
docker build . -f ui.Dockerfile -t alpespartners/ui

echo "[*] Pulling docker-compose dependencies..."
docker-compose pull

echo "[✓] Dev container setup completed successfully."
