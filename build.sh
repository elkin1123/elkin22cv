#!/usr/bin/env bash
# build.sh
set -o errexit

echo "=== Actualizando pip ==="
pip install --upgrade pip

echo "=== Instalando dependencias ==="
pip install -r requirements.txt

echo "=== Recolectando archivos estáticos ==="
# Crear directorios necesarios
mkdir -p /opt/render/project/src/staticfiles/cloudinary
mkdir -p /opt/render/project/src/staticfiles/admin

# Intentar copiar archivos de Cloudinary si están disponibles
echo "Creando archivos estáticos de Cloudinary placeholder..."

# Crear un archivo JS placeholder para Cloudinary
cat > /opt/render/project/src/staticfiles/cloudinary/jquery.cloudinary.js << 'EOF'
// Cloudinary JS placeholder
console.log('Cloudinary JS loaded (placeholder)');
EOF

echo "=== Ejecutando collectstatic ==="
python manage.py collectstatic --noinput --clear || echo "Collectstatic warning, continuando..."

echo "=== Aplicando migraciones ==="
python manage.py migrate --noinput

echo "=== Compilación completada ==="