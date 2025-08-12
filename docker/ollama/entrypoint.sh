#!/bin/sh
set -e

# 1. Arrancar el servidor (en primer plano) en background
ollama serve 2>&1 &          # mantenemos los logs visibles
SERVER_PID=$!

apt update
apt install -y curl

# 2. Esperar a que Ollama responda
echo "⏳ Esperando a que Ollama inicie…"
until curl -sf http://localhost:11434/api/tags >/dev/null ; do
  printf '.'
  sleep 1
done
echo "\n✅ Ollama está en marcha"

# 3. Acciones post-inicio
echo "📝 Descargando modelos… (esto puede tardar)"
ollama pull gpt-oss:20b
ollama pull deepseek-r1:1.5b

# 4. Mantener el contenedor vivo
wait "$SERVER_PID"