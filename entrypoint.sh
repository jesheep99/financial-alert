#!/bin/bash
set -e

# Las variables de GitHub Actions llegan como INPUT_<NAME_EN_MAYUSCULAS>
echo "Starting Financial Tracker & Agent Action..."

# Ejecutar el script principal
python /app/main.py
