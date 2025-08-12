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
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código fuente
COPY . /app

# Expone el puerto en el que FastAPI escuchará (por defecto 8000)
EXPOSE 8000

# Comando para ejecutar la app con Uvicorn al inicio del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
