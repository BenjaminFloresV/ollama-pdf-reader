
import boto3
import asyncio
import traceback
from botocore.client import BaseClient
from app.core.config import AWS_ACCESS_KEY, AWS_REGION, AWS_SECRET_KEY, AWS_BUCKET_NAME

s3_client = None

def init_s3_client():

    global s3_client
    if s3_client is None:
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY,
                aws_secret_access_key=AWS_SECRET_KEY,
                region_name=AWS_REGION,
            )
        except Exception as e:
            traceback.print_exception(e)
            print("Could not connect to s3: {}".format(e))
            return
        
        print("S3 Client initialized")

def get_s3_client() -> BaseClient:
    if s3_client is None:
        raise RuntimeError("S3 client no está inicializado, llama a init_s3_client primero.")
    return s3_client


async def download_bucket_object(object_key: str) -> bytes:
    
    try:
        response = s3_client.get_object(Bucket=AWS_BUCKET_NAME, Key=object_key)
        return response['Body'].read()
    except Exception as e:
        print("Could not download object from s3: {}".format(e))
        return None
    

async def download_bucket_objects(object_keys: list[str]) -> list[bytes]:
    """
        Return: [{'object_key': <object_key>, 's3_url': <s3_url>, 'pdf_bytes': <pdf_bytes>}]
    """
    objects_data = []
    for object_key in object_keys:
        pdf_bytes = await download_bucket_object(object_key)
        s3_url = f'https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/' + object_key
        if not pdf_bytes:
            objects_data.append({
                'object_key': object_key,
                's3_url': s3_url,
                'pdf_bytes': None
            })
            continue
        objects_data.append({
            'object_key': object_key,
            's3_url': s3_url,
            'pdf_bytes': pdf_bytes
        })
    
    return objects_data