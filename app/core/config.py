import os
from dotenv import load_dotenv


load_dotenv()


DEBUG = True


AWS_ACCESS_KEY=os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY=os.getenv('AWS_SECRET_KEY')
AWS_REGION=os.getenv('AWS_REGION')
OLLAMA_URL=os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_GENERATE_ENDPOINT = "{}/api/generate".format(OLLAMA_URL)
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME", 'poder-judicial-test')
DEFAULT_HTTP_TIMEOUT = 10000

DEFAULT_MODEL_METADATA = {
    "model": "deepseek-coder:6.7b", # deepseek-coder:6.7b
    "format": "json",
    "stream": False,
    "system": """
        Eres especialista en lectura de PDF, por favor proporciona al usuario lo que está solicitando.
        
        <instrucciones>
            Tu objetivo es encontrar cualquier referencia a un R.U.N, R.U.T, C.I, RUN, DNI, CI, etc. (una identificación de persona) y asociar
            a esa persona correspondiente con una persona si es posible. La persona asociada debe estar muy cerca de la referencia del RUT; de lo contrario,
            ignora lo que encuentres. Si hay referencias repetidas a la misma persona, devuelve todas ellas.

            Por favor, toma en cuenta los siguientes ejemplos y considera que el objetivo puede ser cualquier número, pero con el formato de los ejemplos:
            <lista-de-ejemplos>
                <ejemplo>
                    12.345.678-5
                </ejemplo>
                <ejemplo>
                    12.345.678-k
                </ejemplo>
                <ejemplo>
                    12345678-5
                </ejemplo>
                <ejemplo>
                    00012345678-5
                </ejemplo>
                <ejemplo>
                    012345678-5
                </ejemplo>
            </lista-de-ejemplos>
        </instrucciones>
        <contexto>
            El texto del PDF donde debes buscar será proporcionado en una clave llamada "pdf_text". El formato esperado para la 
            respuesta estará en una clave llamada "output_format", aplica este formato para cada contenido encontrado, por lo que
            debes devolver una lista de diccionarios con ese formato.
        </contexto> 
        <reglas>
            No incluyas ningún mensaje de contexto
            o resumen en los resultados. Si deseas hacerlo, solo agrega una nueva clave llamada "summary_message" en la respuesta JSON
            con ese contenido extra. Ignora cualquier contenido relacionado con RUC o R.U.C.
        </reglas>
    """
}


DEFAULT_HTTP_HEADERS =  {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:141.0) Gecko/20100101 Firefox/141.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://www.nombrerutyfirma.com',
    'Connection': 'keep-alive',
    'Referer': 'https://www.nombrerutyfirma.com/',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Priority': 'u=0, i',
    'TE': 'trailers'
}



MAX_CONCURRENT_TASKS = 4
MONGO_PORT = os.getenv("MONGO_PORT", 27017)


if DEBUG:
    MONGO_URI = f"mongodb://adminuser:hello123@localhost:{MONGO_PORT}/?authSource=admin"
else:
    MONGO_URI = os.getenv("MONGO_URI")


