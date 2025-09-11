#!/bin/bash

echo "[*] Installing Python dependencies..."
pip install -r requirements.txt

echo "[*] Building Docker images..."
docker build . -f alpespartners.Dockerfile -t alpespartners/flask

echo "[*] Pulling docker-compose dependencies..."
docker-compose pull

echo "[✓] Dev container setup completed successfully."
