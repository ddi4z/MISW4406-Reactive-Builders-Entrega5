#!/bin/bash

# Ruta base de tus directorios
BASE_DIR="./data"

# Directorios a resetear
DIRS=("bookkeeper" "postgres" "zookeeper" "postgres_eventos")

echo "🔄 Reseteando directorios en $BASE_DIR ..."

for d in "${DIRS[@]}"; do
  TARGET="$BASE_DIR/$d"

  # Eliminar si existe
  if [ -d "$TARGET" ]; then
    echo "🗑️  Eliminando $TARGET ..."
    sudo rm -rf "$TARGET"
  fi

  # Crear de nuevo
  echo "📂 Creando $TARGET ..."
  sudo mkdir -p "$TARGET"

  # Permisos y ownership
  echo "🔑 Ajustando permisos y propietario en $TARGET ..."
  sudo chmod 777 "$TARGET"
  sudo chown root:root "$TARGET"
done

echo "✅ Directorios reseteados correctamente."
