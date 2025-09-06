FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Variables de entorno recomendadas para evitar problemas de buffer y bytecode
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Actualiza los repositorios y herramientas necesarias (ejemplo: gcc para compilar dependencias)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requerimientos y instala las dependencias
COPY ./requirements.txt /app/requirements.txt
# Instala dependencias de producción y testing
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir pytest pytest-asyncio

# Copia el resto del código fuente (incluyendo tests)
COPY . /app

# Copia el entrypoint que correrá los tests y luego iniciará la app
COPY ./docker/fastapi/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Expone el puerto en el que FastAPI escuchará (por defecto 8000)
EXPOSE 8000

# Comando por defecto: ejecutar entrypoint (tests + API)
CMD ["/app/entrypoint.sh"]
