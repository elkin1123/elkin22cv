# Crea el archivo build.sh correctamente
cat > build.sh << 'EOF'
#!/usr/bin/env bash
set -o errexit

echo "=== Actualizando pip ==="
pip install --upgrade pip

echo "=== Instalando dependencias ==="
pip install -r requirements.txt

echo "=== Aplicando migraciones ==="
python manage.py migrate

echo "=== Recolectando archivos estáticos ==="
python manage.py collectstatic --noinput

echo "=== Verificando la app ==="
python manage.py check --deploy --fail-level WARNING

echo "✅ Build completado exitosamente!"
EOF

# Dale permisos de ejecución
chmod +x build.sh