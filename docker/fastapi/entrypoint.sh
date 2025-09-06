#!/bin/sh
set -e

# ── Ejecutar tests unitarios ─────────────────────────────────────────
pytest 
# ── Lanzar la aplicación FastAPI ──────────────────────────────────── ─
exec uvicorn main:app --host 0.0.0.0 --port 8000
