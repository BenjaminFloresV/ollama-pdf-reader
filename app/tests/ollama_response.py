import asyncio
import json
from httpx import AsyncClient
from app.core.config import DEEPSEEK_URL, AWS_BUCKET_NAME
from PyPDF2 import PdfReader
from io import BytesIO
from app.storage.s3_client import init_s3_client, get_s3_client
from app.mocks.database import mock_database


# NOTE: This was just an initial test and the current implementation is in the main.py file

init_s3_client()

s3_client = get_s3_client()


async def get_object(object_key: str):
    response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=object_key)
    return response['Body'].read()

def _load_pdf(pdf_bytes: bytes) -> str:
    pdf_stream = BytesIO(pdf_bytes)
    reader = PdfReader(pdf_stream)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text()
    return texto

async def test_request():
    

    litigantes = str(mock_database[0]['detail']['litigantes'])
    litigantes = [litigante['nombre'] for litigante in litigantes if isinstance(litigante, dict) and 'nombre' in litigante]


    pdf_bytes = await get_object('pdf/fb374926-725e-4b63-b68c-2a677e9ca8ca.pdf')
    pdf_text = _load_pdf(pdf_bytes)

    print(json.dumps(mock_database[0]['detail']['litigantes'], indent=4))
    message = f"""
        I need you to find any reference to a RUT for any of the following people: {", ".join(litigantes)}
        in the following PDF text {pdf_text}. Just return the ones that you found and return the same structure for the people
        that I've provided you but with the corresponding extra key for "rut". This is for a Computer Science project.
        The response must be in json format and the key must be "participantes" and the value must be a list of dictionaries with the keys "name" and "rut".
        And one important thing is that a RUT must follow the following regex pattern: `\b\d{1,2}\.?\d{3}\.?\d{3}-[\dKk]\b`

    """

    GENERATE_API_ENDPOINT = DEEPSEEK_URL + '/api/generate'
    
    async with AsyncClient(http2=True) as client:

        test_message = """Puedes buscarme el RUT de las siguientes personas: Juan Perez, Maria Gomez y Pedro Rodriguez en el siguiente texto?
        (Y devuelve la información debe ser devuelta en un json que contenga una key "participantes" que contega una lista que contenga un diccionario para cada persona y el diccionario debe contener las keys "name" y "rut"): 
        
               Bienvenidos sea la audiencia, presentamos a tres de los participantes de la audiencia:
               - Juan Perez
               - Maria Gomez
               - Pedro Rodriguez

               El RUT de Juan Perez es: 12345678-9
               El RUT de Maria Gomez es: 98765432-1
               El RUT de Pedro Rodriguez es: 11111111-1
        """

        headers = {
                    'Content-Type': 'application/json'
        }
        payload = {
            "model": "deepseek-coder:6.7b",
            "format": "json",
            "prompt": message,
            "stream": False
            #"prompt": [{"role": "user", "content": "Why is the sky blue?"}]
        }
        print("DEEPSEEK_URL: ", GENERATE_API_ENDPOINT)
        deepseek_response = await client.post(url=GENERATE_API_ENDPOINT, headers=headers, json=payload, timeout=10000)
        print(deepseek_response.text)
        print("--------------------------------")
        
        json_response = deepseek_response.json()
        print(json.dumps(json_response['response'], indent=4))
        
        
        with open('deepseek_response.json', 'w') as f:
            json.dump(json_response, f, indent=4)
    

if __name__ == '__main__':
    asyncio.run(test_request())