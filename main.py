

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from app.models.causa import CausaItem
from app.storage.s3_client import init_s3_client, get_s3_client
from app.mocks.database import mock_database
import app.services.ollama as ollame_service


# To check API doc: 
# - http://127.0.0.1:8000/redoc
# - http://127.0.0.1:8000/docs#/default/update_item_items__item_id__put (SwaggerUI)


s3 = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load whatever you need, example: db client
    init_s3_client()
    s3['client'] = get_s3_client

    await ollame_service.pull_model('deepseek-r1:1.5b')
    await ollame_service.pull_model('deepseek-coder:6.7b')
    await ollame_service.pull_model('gpt-oss:20b')

    yield
    # Clean up the ML models and release the resources when server shutsdown
    s3.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/causas/process-pdfs", status_code=200)
async def process_associated_pdfs(test: str | None = None, item: CausaItem | None = None, response: Response = Response):
    
    if test == 'true':
    
        causa_id = item.causa_id
        causa = None
        for row in mock_database:
            if row['id'] == causa_id:
                causa = row
            
                break

        if not causa:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"message": "Causa does not exist"}
        
        ollama_responses = []

        s3_urls = [pdf['s3_url'] for pdf in causa['detail']['associated_pdfs']]
        object_keys = [ 'pdf/' + s3_url.split('/')[-1] for s3_url in s3_urls]
        
        ollama_responses = await ollame_service.extract_ruts_from_pdf(causa['detail']['litigantes'], object_keys, use_async=True)

        failed_responses = [response for response in ollama_responses if response['result'] is None]
        success_responses = [response for response in ollama_responses if response['result'] is not None]
        
        print("Done.")
        return {'success_responses': success_responses, 'failed_responses': failed_responses}

    return {"message": "You need to implement this endpoint"}