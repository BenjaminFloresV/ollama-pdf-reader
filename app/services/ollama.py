

import json
import asyncio
from app.storage.s3_client import download_bucket_object
from app.utils.pdf import load_pdf_with_text_extraction
from app.core.config import OLLAMA_GENERATE_ENDPOINT, DEFAULT_MODEL_METADATA, OLLAMA_URL
from app.core.http import fetcher



async def pull_model(model_name: str = 'deepseek-r1:1.5b'):
    payload = {
        'model': model_name,
        'stream': False,
        'format': 'json'
    }
    response, status_code = await fetcher.post(OLLAMA_URL + '/api/pull', data=payload, headers={"Content-Type": "application/json"})
    if status_code != 200:
        raise Exception(f"Could not pull model: {response}")
    return response


async def fetch_model(prompt: str, paylaod: dict = DEFAULT_MODEL_METADATA) -> dict:
    payload = paylaod.copy()
    payload['prompt'] = prompt
    
    response, status_code = await fetcher.post(OLLAMA_GENERATE_ENDPOINT, data=payload, headers={"Content-Type": "application/json"})
    
    if status_code != 200:
        raise Exception("Could not fetch model")
    return response



async def extract_ruts_from_pdf(litigantes: list[dict], object_keys: list[str], use_async: bool = False) -> list[dict]:
    tasks = []
    for object_key in object_keys:
        if use_async:
            tasks.append(_extract_ruts_from_pdf(litigantes, object_key))
        else:
            tasks.append(asyncio.to_thread(_extract_ruts_from_pdf, litigantes, object_key))

    if use_async:
        return await asyncio.gather(*tasks)
    else:
        return [task.result() for task in tasks]


async def _extract_ruts_from_pdf(litigantes: list[dict], pdf_object_key: str, model_metadata: dict = DEFAULT_MODEL_METADATA) -> list[dict]:
    
    try:
        print(f"Downloading PDF: {pdf_object_key}")
        pdf_bytes = await download_bucket_object(pdf_object_key)
        
        if pdf_bytes is None:
            raise Exception("Could not download object from s3")

        pdf_text = load_pdf_with_text_extraction(pdf_bytes)
        message = f"""
            I need you to find any reference to a RUT for any of the following people: {json.dumps(litigantes, indent=4)}
            in the following PDF text {pdf_text}. Just return the ones that you found and return the same structure for the people
            that I've provided you but with the corresponding extra key for "rut". This is for a Computer Science project.
            The response must be in json format and the key must be "participantes" and the value must be a list of dictionaries with the same keys as the input plus the key "rut" with the value of the RUT (if found).
            And one important thing is that a RUT must follow the following regex pattern: `\b\d{1,2}\.?\d{3}\.?\d{3}-[\dKk]\b` and please DO NOT CHANGE the original key names of the input, just add the new key "rut" to the output.

        """
        print(f"Processing PDF: {pdf_object_key}")
        response = await fetch_model(message, model_metadata)
        return {'result': json.loads(response['response']), 'object_key': pdf_object_key}
    except Exception as e:
        print(f"Error extracting RUTs from PDF: {e}")
        return {'result': None, 'object_key': pdf_object_key}


async def ollama_generate_endpoint():
    test_message = "Hello, how are you?"
    response = await fetch_model(test_message)
    print(response)


if __name__ == "__main__":
    asyncio.run(ollama_generate_endpoint())
    
    
    
    