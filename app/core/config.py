import os
from dotenv import load_dotenv


load_dotenv()



AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_REGION=os.getenv('AWS_REGION')
OLLAMA_URL=os.getenv('DEEPSEEK_URL', 'http://localhost:11434')
OLLAMA_GENERATE_ENDPOINT = "{}/api/generate".format(OLLAMA_URL)
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", 'poder-judicial-test')
DEFAULT_HTTP_TIMEOUT = 10000

DEFAULT_MODEL_METADATA = {
    "model": "deepseek-coder:6.7b", # deepseek-coder:6.7b
    "format": "json",
    "stream": False
}