#!/bin/bash
set -e

# Las variables de GitHub Actions llegan como INPUT_<NAME_EN_MAYUSCULAS>
# Ejemplo de configuración recibida:
# INPUT_TICKERS="IVV,BTC-USD"
# INPUT_ENABLE_README="true"
# INPUT_ENABLE_TELEGRAM="false"
# INPUT_ENABLE_EMAIL="false"
# INPUT_TELEGRAM_TOKEN y INPUT_TELEGRAM_CHAT_ID también llegan como variables
# de entorno; no imprimir sus valores porque pueden contener datos sensibles.
# Python hereda estas variables y main.py las lee con os.environ.
echo "Starting Financial Tracker & Agent Action..."

# Ejecutar el script principal
python /app/main.py
