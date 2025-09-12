

# curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
#   -H 'Content-Type: application/json' \
#  -H 'X-goog-api-key: AIzaSyDXD6whPkFZzZqWrRQqNPzCa564cX7Cueg' \
#   -X POST \
#   -d '{
#    "contents": [
#      {
#        "parts": [
#          {
#            "text": "Explain how AI works in a few words"
#          }
#        ]
#      }
#    ]
#  }'


import httpx
import asyncio
import traceback
from google import genai
from pydantic import BaseModel
from google.genai import types
from app.core.config import GEMINI_API_KEY
from app.services.base import BaseService
from app.core.logger import StructuredLogger

logger = StructuredLogger(service="gemini_api")

client = genai.Client(
    api_key=GEMINI_API_KEY,
)

class Litigante(BaseModel):
    name: str
    rut: str




pdf1 = "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/960f2834-d11e-429e-a559-90e417c66d5c.pdf"
pdf2= "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/3f80462e-4e98-4855-8140-19e9dfe7232e.pdf"
pdf3= "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/68144e51-d93f-49bd-bbd4-86c9307952dc.pdf"
pdf4= "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/ff902720-f530-4d1e-995a-981bca0a71a9.pdf"
pdf5 = "https://poder-judicial-test.s3.us-east-1.amazonaws.com/pdf/fd23f4b8-ff15-47da-b4e4-595d429728a3.pdf"
doc_url = pdf5

# Retrieve and encode the PDF byte
class GeminiAPI(BaseService):
    
    def __init__(self):
        self.client = client
    
    
    def extract_ruts_from_pdf(self, doc_url: str):
        """
        Extract RUTs from a PDF document using Gemini API
        Args:
            doc_url: URL of the PDF document
        Returns:
            List of dictionaries with name and RUT
        """
        try:
            logger.info("Extracting RUTs from PDF", extra={"doc_url": doc_url})
            
            # Download PDF content synchronously
            doc_data = httpx.get(doc_url).content

            prompt = "Extract the RUTs (also called 'Cédula de Identidad', 'RUT', 'R.U.T.', 'RUT', 'C.I.' or 'R.U.T.') of the people in the document"
            
            # Use synchronous Gemini client
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=doc_data,
                        mime_type='application/pdf',
                    ),
                    prompt],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[Litigante],
                },  
            )
            
            json_response = response.model_dump()
            total_tokens = json_response['usage_metadata']['total_token_count']
            
            logger.info("Gemini API response", extra={"json_response": json_response})
            logger.info("Total tokens", extra={"total_tokens": total_tokens})
            
            return {
                'result': json_response['parsed'],
                'status': 'ok',
                'message': 'PDF file processed',
                's3_url': doc_url
            }
            
        except Exception as e:
            logger.error("Error extracting RUTs from PDF", extra={"error": str(e)})
            return {
                'result': None,
                'status': 'error',
                'error': str(e) + "traceback: " + traceback.format_exc(),
                's3_url': doc_url
            }

    async def extract_ruts_from_pdf_async(self, doc_urls: list[str]):
        """
        Asynchronous version to process multiple URLs
        """
        tasks = []
        for doc_url in doc_urls:
            # Execute synchronous function in executor to avoid blocking
            task = asyncio.get_event_loop().run_in_executor(
                None, self.extract_ruts_from_pdf, doc_url
            )
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        return results


if __name__ == "__main__":
    gemini_api = GeminiAPI()
    # Execute synchronous function directly
    #result = gemini_api.extract_ruts_from_pdf(doc_url)
    #print(f"Result: {result}")
    # Execute asynchronous function directly
    result_async = asyncio.run(gemini_api.extract_ruts_from_pdf_async([doc_url, doc_url]))
    print(f"Asynchronous result: {result_async}")