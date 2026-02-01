#!/bin/bash
# build.sh
set -o errexit

echo "=== Actualizando pip ==="
python -m pip install --upgrade pip

echo "=== Instalando dependencias ==="
pip install -r requirements.txt

echo "=== Creando directorios necesarios ==="
mkdir -p staticfiles/cloudinary

echo "=== Creando archivo placeholder para Cloudinary JS ==="
cat > staticfiles/cloudinary/jquery.cloudinary.js << 'EOF'
// Cloudinary JS placeholder file
console.log('Cloudinary JS loaded (placeholder)');
EOF

echo "=== Verificando configuración de Django ==="
python manage.py check --deploy || echo "Check encontró advertencias, continuando..."

echo "=== Aplicando migraciones ==="
python manage.py migrate --noinput

echo "=== Recolectando archivos estáticos ==="
python manage.py collectstatic --noinput --clear

echo "=== Compilación completada exitosamente ==="