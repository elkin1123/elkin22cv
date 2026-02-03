#!/usr/bin/env bash
# build.sh - VERSIÓN CORREGIDA CON TODOS LOS TYPOS
set -o errexit

echo "=== ACTUALIZANDO PIP ==="
pip install --upgrade pip

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== CORRIGIENDO TODOS LOS TYPOS EN POSTGRESQL ==="
# Corregir todos los typos en los nombres de columnas
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_elkin.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # 1. Corregir ExperienciaLaboral - typo en ForeignKey
        try:
            cursor.execute('''
                ALTER TABLE tasks_experiencialaboral 
                RENAME COLUMN idperfilconqueestaativo_id 
                TO idperfilconqueestaactivo_id;
            ''')
            print('✓ Columna de ExperienciaLaboral corregida')
        except Exception as e:
            print(f'⚠️  Error corrigiendo ExperienciaLaboral: {e}')
        
        # 2. Corregir ProductoAcademico
        try:
            cursor.execute('''
                ALTER TABLE tasks_productoacademico 
                RENAME COLUMN IF EXISTS activarparaqueseveaenfront 
                TO activarparaqueseveaenfront;
            ''')
            print('✓ Columna de ProductoAcademico corregida')
        except Exception as e:
            print(f'⚠️  Error corrigiendo ProductoAcademico: {e}')
        
        # 3. Corregir VentaGarage
        try:
            cursor.execute('''
                ALTER TABLE tasks_ventagarage 
                RENAME COLUMN IF EXISTS nombrepreducto 
                TO nombreproducto;
            ''')
            print('✓ Columna de VentaGarage corregida')
        except Exception as e:
            print(f'⚠️  Error corrigiendo VentaGarage: {e}')
        
        # 4. Verificar y corregir todas las tablas relacionadas
        tablas = ['productoacademico', 'productolaboral', 'cursorealizado', 'reconocimiento']
        for tabla in tablas:
            try:
                cursor.execute(f'''
                    ALTER TABLE tasks_{tabla} 
                    RENAME COLUMN idperfilconqueestaativo_id 
                    TO idperfilconqueestaactivo_id;
                ''')
                print(f'✓ Columna de {tabla} corregida')
            except Exception as e:
                print(f'⚠️  Error corrigiendo {tabla}: {e}')
                
except Exception as e:
    print(f'⚠️  Error general: {e}')
    print('⚠️  Continuando con la construcción...')
"

echo "=== APLICANDO MIGRACIONES ==="
python manage.py makemigrations
python manage.py migrate

echo "=== VERIFICANDO BASE DE DATOS ==="
python manage.py shell << EOF
from django.db import connection

with connection.cursor() as cursor:
    # Verificar todas las columnas
    cursor.execute("""
        SELECT table_name, column_name, data_type 
        FROM information_schema.columns 
        WHERE table_schema = 'public' 
        AND table_name LIKE 'tasks_%'
        ORDER BY table_name, column_name;
    """)
    
    print("=== COLUMNAS EN LA BASE DE DATOS ===")
    for row in cursor.fetchall():
        print(f"{row[0]}.{row[1]} ({row[2]})")
EOF

echo "=== COLECTANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --no-input

echo "=== CONSTRUCCIÓN COMPLETADA ==="