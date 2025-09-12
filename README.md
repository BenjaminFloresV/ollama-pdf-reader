# Ollama PDF Reader - Extractor de RUTs

Sistema de extracción automatizada de RUTs (Rol Único Tributario) de documentos PDF utilizando modelos de IA locales (Ollama) y servicios en la nube (Gemini API).

## 📋 Descripción

Este proyecto es una API REST desarrollada en FastAPI que permite procesar documentos PDF asociados a causas judiciales para extraer automáticamente los RUTs de personas naturales mencionadas en los documentos. El sistema utiliza múltiples enfoques de procesamiento:

- **Ollama**: Modelos de IA locales para análisis de texto
- **Gemini API**: Servicio de Google para procesamiento de documentos
- **Expresiones regulares**: Extracción tradicional por patrones
- **AWS S3**: Almacenamiento de documentos PDF

## 🚀 Características

- ✅ Extracción automática de RUTs de documentos PDF
- ✅ Múltiples métodos de procesamiento (Ollama, Gemini, RegEx)
- ✅ Validación de RUTs chilenos
- ✅ Procesamiento asíncrono para mejor rendimiento
- ✅ Integración con AWS S3 para almacenamiento de documentos
- ✅ Base de datos MongoDB para persistencia
- ✅ Containerización con Docker
- ✅ Logging estructurado
- ✅ API REST documentada con OpenAPI/Swagger

## 🏗️ Arquitectura

```
├── app/
│   ├── core/           # Configuración y utilidades centrales
│   ├── models/         # Modelos de datos Pydantic
│   ├── services/       # Lógica de negocio
│   │   ├── ollama.py          # Integración con Ollama
│   │   ├── gemini_api.py      # Integración con Gemini API
│   │   └── pdf_reader.py      # Procesamiento de PDFs
│   ├── storage/        # Integración con AWS S3
│   ├── persistence/    # Acceso a base de datos
│   ├── utils/          # Utilidades y helpers
│   └── tests/          # Tests unitarios
├── docker/             # Configuraciones de Docker
├── main.py            # Aplicación principal FastAPI
└── docker-compose.yml # Orquestación de servicios
```

## 🛠️ Tecnologías

- **Backend**: Python 3.10+, FastAPI, Uvicorn
- **IA/ML**: Ollama (DeepSeek Coder), Google Gemini API
- **Base de datos**: MongoDB
- **Almacenamiento**: AWS S3
- **Procesamiento PDF**: PyMuPDF, PyPDF2, pdf2image, pytesseract
- **Containerización**: Docker, Docker Compose
- **Testing**: pytest, pytest-asyncio

## 📦 Instalación

### Prerrequisitos

- Python 3.10+
- Docker y Docker Compose
- GPU NVIDIA (opcional, para acelerar Ollama)

### Configuración del entorno

1. **Clonar el repositorio**:
```bash
git clone <repository-url>
cd ollama_pdf_reader
```

2. **Crear archivo de configuración**:
```bash
cp env-example .env
```

3. **Configurar variables de entorno** (`.env`):
```env
# AWS Configuration
AWS_ACCESS_KEY=tu_access_key
AWS_SECRET_KEY=tu_secret_key
AWS_REGION=us-east-1

# MongoDB Configuration
TEST_MONGO_USER=adminuser
TEST_MONGO_PASSWORD=hello123
TEST_MONGO_PORT=27017
PRODUCTION_MONGO_URI=mongodb://...

# API Configuration
FAST_API_PORT=8000
OLLAMA_API_REST_PORT=11434

# AI Configuration
GEMINI_API_KEY=tu_gemini_api_key
USE_GPT_OSS=false

# Debug
DEBUG=true
```

### Instalación con Docker (Recomendado)

```bash
# Construir y ejecutar todos los servicios
docker-compose up --build

# Ejecutar en segundo plano
docker-compose up -d
```

### Instalación manual

1. **Crear entorno virtual**:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Instalar y configurar Ollama**:
```bash
# Instalar Ollama (https://ollama.ai)
curl -fsSL https://ollama.ai/install.sh | sh

# Descargar modelos
ollama pull deepseek-coder:6.7b
ollama pull gpt-oss:20b  # opcional
```

4. **Ejecutar la aplicación**:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔧 Uso

### API Endpoints

#### Health Check
```http
GET /health
```

#### Procesar PDFs de una causa
```http
POST /causas/process-pdfs
Content-Type: application/json

{
    "causa_id": "12345",
    "test": "true",
    "model": "deepseek-coder:6.7b"
}
```

### Documentación de la API

Una vez ejecutándose, accede a:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Ejemplo de respuesta

```json
{
    "ollama_responses": {
        "success_responses": [
            {
                "result": {
                    "resultados": [
                        {
                            "nombre": "Juan Pérez García",
                            "rut": "12.345.678-5"
                        }
                    ]
                },
                "status": "ok",
                "message": "PDF file processed",
                "s3_url": "https://..."
            }
        ],
        "failed_responses": []
    },
    "pdf_reader_response": ["12345678-5", "98765432-1"],
    "pdfs_without_text": []
}
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Ejecutar tests con cobertura
pytest --cov=app

# Ejecutar tests específicos
pytest app/tests/test_validate_ruts.py
```

## 🔍 Servicios

### OllamaService
- Integración con modelos locales de Ollama
- Extracción de RUTs usando IA generativa
- Procesamiento asíncrono de múltiples documentos

### GeminiAPI
- Integración con Google Gemini API
- Procesamiento directo de PDFs
- Extracción estructurada con esquemas Pydantic

### PDFReaderService
- Conversión de bytes PDF a texto
- Extracción por expresiones regulares
- Validación de RUTs chilenos

## 📊 Monitoreo y Logs

El sistema utiliza logging estructurado para facilitar el monitoreo:

```python
logger = StructuredLogger(service="extract-ruts-from-pdf")
logger.info("Request received", extra={"causa_id": "12345"})
```

## 🐳 Docker

### Servicios incluidos

- **ollama_server**: Servidor Ollama con GPU support
- **fastapi_app**: Aplicación principal
- **mongo**: Base de datos MongoDB

### Comandos útiles

```bash
# Ver logs
docker-compose logs -f fastapi_app

# Reiniciar un servicio
docker-compose restart ollama_server

# Escalar servicios
docker-compose up --scale fastapi_app=2
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🔧 Configuración avanzada

### Modelos de Ollama

El sistema soporta múltiples modelos:
- `deepseek-coder:6.7b` (por defecto)
- `gpt-oss:20b` (opcional)

### Configuración de GPU

Para usar GPU con Ollama, asegúrate de tener:
- NVIDIA Container Toolkit instalado
- Descomenta las líneas de GPU en `docker-compose.yml`

### Variables de entorno adicionales

```env
MAX_CONCURRENT_TASKS=4
DEFAULT_HTTP_TIMEOUT=10000
AWS_BUCKET_NAME=poder-judicial-test
```

## 🚨 Troubleshooting

### Problemas comunes

1. **Error de conexión a Ollama**:
   ```bash
   # Verificar que Ollama esté ejecutándose
   docker-compose logs ollama_server
   ```

2. **Modelos no encontrados**:
   ```bash
   # Descargar modelos manualmente
   docker exec -it ollama_server ollama pull deepseek-coder:6.7b
   ```

3. **Errores de memoria**:
   - Reduce el número de tareas concurrentes
   - Usa modelos más pequeños
   - Aumenta la memoria disponible para Docker

## 📞 Soporte

Para soporte y preguntas:
- Revisa la documentación de la API en `/docs`
- Consulta los logs estructurados para debugging
