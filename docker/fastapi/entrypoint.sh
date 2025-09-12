#!/bin/sh
set -e

FAST_API_PORT=${FAST_API_PORT}

# ── Ejecutar tests unitarios ─────────────────────────────────────────
pytest 
# ── Lanzar la aplicación FastAPI ──────────────────────────────────── ─
exec uvicorn main:app --host 0.0.0.0 --port ${FAST_API_PORT}
