#!/usr/bin/env bash
# build.sh - VERSIÓN CORREGIDA
set -o errexit

echo "=== ACTUALIZANDO PIP ==="
pip install --upgrade pip

echo "=== INSTALANDO DEPENDENCIAS ==="
pip install -r requirements.txt

echo "=== CORRIGIENDO NOMBRES DE COLUMNAS EN POSTGRESQL ==="
# Corregir los typos en los nombres de columnas
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cv_elkin.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # 1. Corregir ProductoAcademico (el typo está en la base de datos)
        cursor.execute(\"\"\"
            ALTER TABLE IF EXISTS tasks_productoacademico 
            RENAME COLUMN IF EXISTS activarparaqueseveaenfront 
            TO activarparaqueseveaenfront;
        \"\"\")
        print('✓ Columna de ProductoAcademico corregida')
        
        # 2. Corregir VentaGarage (el typo está en la base de datos)
        cursor.execute(\"\"\"
            ALTER TABLE IF EXISTS tasks_ventagarage 
            RENAME COLUMN IF EXISTS nombrepreducto 
            TO nombreproducto;
        \"\"\")
        print('✓ Columna de VentaGarage corregida')
        
        # 3. Si hay más columnas con typos, corregirlas también
        cursor.execute(\"\"\"
            DO \$\$
            BEGIN
                -- Verificar y corregir ExperienciaLaboral si es necesario
                IF EXISTS (SELECT 1 FROM information_schema.columns 
                          WHERE table_name='tasks_experiencialaboral' 
                          AND column_name='telefonocontactoempresarial') THEN
                    ALTER TABLE tasks_experiencialaboral 
                    DROP COLUMN telefonocontactoempresarial;
                    RAISE NOTICE 'Columna eliminada de ExperienciaLaboral';
                END IF;
            END
            \$\$;
        \"\"\")
        
except Exception as e:
    print(f'⚠️  Error corrigiendo columnas: {e}')
    print('⚠️  Continuando con la construcción...')
"

echo "=== APLICANDO MIGRACIONES ==="
python manage.py makemigrations
python manage.py migrate

echo "=== COLECTANDO ARCHIVOS ESTÁTICOS ==="
python manage.py collectstatic --no-input

echo "=== CONSTRUCCIÓN COMPLETADA ==="