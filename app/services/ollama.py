

import json
import asyncio
from app.storage.s3_client import download_bucket_object
from app.utils.pdf import load_pdf_with_text_extraction
from app.core.config import OLLAMA_GENERATE_ENDPOINT, DEFAULT_MODEL_METADATA, OLLAMA_URL, AWS_BUCKET_NAME, AWS_REGION
from app.core.http import fetcher



async def pull_model(model_name: str = 'deepseek-r1:1.5b'):
    payload = {
        'model': model_name,
        'stream': False,
        'format': 'json'
    }
    response, status_code = await fetcher.post(OLLAMA_URL + '/api/pull', data=payload, headers={"Content-Type": "application/json"})
    if status_code != 200:
        print(status_code)
        raise Exception(f"Could not pull model: {response}")
    return response


async def fetch_model(prompt: str, paylaod: dict = DEFAULT_MODEL_METADATA) -> dict:
    payload = paylaod.copy()
    payload['prompt'] = prompt
    
    response, status_code = await fetcher.post(OLLAMA_GENERATE_ENDPOINT, data=payload, headers={"Content-Type": "application/json"})
    
    if status_code != 200:
        raise Exception("Could not fetch model")
    return response



async def extract_ruts_from_pdf(litigantes: list[dict], object_keys: list[str], use_async: bool = False, model: str = 'deepseek-coder:6.7b') -> list[dict]:
    tasks = []
    for object_key in object_keys:
        if use_async:
            tasks.append(_extract_ruts_from_pdf(litigantes, object_key, model=model))
        else:
            tasks.append(_extract_ruts_from_pdf(litigantes, object_key, model=model))

    if use_async:
        return await asyncio.gather(*tasks)
    else:
        return [task.result() for task in tasks]


async def _extract_ruts_from_pdf(
    litigantes: list[dict],
    pdf_object_key: str,
    model_metadata: dict = DEFAULT_MODEL_METADATA,
    model: str = 'deepseek-coder:6.7b') -> list[dict]:
    
    print(model_metadata)
    model_metadata['model'] = model
    
    try:
        print(f"Downloading PDF: {pdf_object_key}")
        pdf_bytes = await download_bucket_object(pdf_object_key)
        
        if pdf_bytes is None:
            raise Exception("Could not download object from s3")

        pdf_text = load_pdf_with_text_extraction(pdf_bytes)
        message = f"""
            I need you to find any reference to a RUT or Identificador for any of the following people: {json.dumps(litigantes, indent=4)}
            in the following PDF text {pdf_text}. 
            
            Just return the ones that you found that matches the provided people that I've provided you but with the corresponding extra key for "rut". This is for a Computer Science project.
            The response must be in json format and the key must be "participantes" and the value must be a list of dictionaries with the same keys as the input plus the key "rut" with the value of the RUT (if found).
            And one important thing is that please DO NOT CHANGE the original key names of the input, just add the new key "rut" to the output.
            If you don't find any RUT, return an empty list for the "participantes" key and If you found some RUTs, return the same structure for the people that I've provided you but with the corresponding extra key for "rut" and
            do not add the "rut" key to the people that you didn't find a RUT for. Any extra message that you want to add, add it in the end of the response.

        """
        print(f"Processing PDF: {pdf_object_key}")
        response = await fetch_model(message, model_metadata)
        # https://poder-judicial-test.s3.us-east-2.amazonaws.com/
        return {
            'result': json.loads(response['response']),
            'object_key': pdf_object_key,
            's3_path': f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{pdf_object_key}"
        }
    except Exception as e:
        print(f"Error extracting RUTs from PDF: {e}")
        return {'result': None, 'object_key': pdf_object_key}


async def ollama_generate_endpoint():
    test_message = "Hello, how are you?"
    response = await fetch_model(test_message)
    print(response)


if __name__ == "__main__":
    asyncio.run(ollama_generate_endpoint())
    
    
    
    