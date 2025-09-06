

from contextlib import asynccontextmanager
from fastapi import FastAPI, Response, status
from app.models.causa import CausaItem
from app.mocks.database import mock_database
from app.services.ollama import OllamaService
from app.services.pdf_reader import PDFReaderService
from app.storage.s3_client import init_s3_client, download_bucket_objects
from app.persistence.persistence import persistence as persistence_client

# To check API doc: 
# - http://127.0.0.1:8000/redoc
# - http://127.0.0.1:8000/docs#/default/update_item_items__item_id__put (SwaggerUI)


ollama_service = OllamaService()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load whatever you need, example: db client
    init_s3_client() 
    #await ollame_service.pull_model('deepseek-r1:1.5b')
    await ollama_service.pull_model('deepseek-coder:6.7b')
    #await ollame_service.pull_model('gpt-oss:20b')

    yield
    # Anyhing else at the end


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/causas/process-pdfs", status_code=200)
async def process_associated_pdfs(
    test: str | None = None,
    model: str | None = None,
    item: CausaItem | None = None,
    response: Response = Response
):
    
    if test == 'true':
    
        causa_id = item.causa_id
        causa = None
        for row in mock_database:
            if row['id'] == causa_id:
                causa = row
            
                break
        
    else:
        causa = await persistence_client.get_causa_by_id(item.causa_id)
        
        
    if not causa:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"message": "Causa does not exist"}

    ollama_responses = []

    is_reserved = causa['detail']['is_reserved']
    if is_reserved:
        return {'success_responses': [], 'failed_responses': [], 'message': 'Causa is reserved'}

    s3_urls = [pdf['s3_url'] for pdf in causa['detail']['associated_pdfs']]
    object_keys = [ 'pdf/' + s3_url.split('/')[-1] for s3_url in s3_urls]
    objects_metadata = await download_bucket_objects(object_keys)
    
    pdf_reader = PDFReaderService(objects_metadata)
    pdfs_data = await pdf_reader.get_pdfs_data()
    
    pdfs_with_text = [pdf_data for pdf_data in pdfs_data if pdf_data['pdf_text']]
    pdfs_without_text = [pdf_data for pdf_data in pdfs_data if not pdf_data['pdf_text']]

    ollama_responses = await ollama_service.extract_ruts_from_pdf(
        causa['detail']['litigantes'], pdfs_with_text, use_async=True, model=model)

    failed_responses = [response for response in ollama_responses if response['result'] is None]
    success_responses = [response for response in ollama_responses if response['result'] is not None]
    

    print("Done.")
    return {'success_responses': success_responses, 'failed_responses': failed_responses, 'pdfs_without_text': pdfs_without_text}

