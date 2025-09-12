import re
import asyncio
from app.services.base import BaseService
from app.utils.pdf import load_pdf
from app.utils.toolbelt import validate_rut
from app.core.logger import StructuredLogger

logger = StructuredLogger(service="pdf_reader_service")

class PDFReaderService(BaseService):
    
    def __init__(self, pdf_files_data: list):
        self.transformed_pdf_files = self._transform_pdf_bytes_to_text(pdf_files_data)

    def _transform_pdf_bytes_to_text(self, pdf_files_data: list) -> list:
        
        transformed_pdfs = []
        for pdf_data in pdf_files_data:
            if not pdf_data['pdf_bytes']:
                transformed_pdfs.append({'status': 'error', 'pdf_text': '', **pdf_data})
                continue
            pdf_text = load_pdf(pdf_data['pdf_bytes'])
            if not pdf_text:
                transformed_pdfs.append({'status': 'error', 'pdf_text': '', **pdf_data})
            transformed_pdfs.append({'status': 'success', 'pdf_text': pdf_text, **pdf_data})
            
        for pdf_data in transformed_pdfs:
            del pdf_data['pdf_bytes']

        return transformed_pdfs
    
    
    async def get_pdfs_data(self):
        """
            return: [{'status': <status>, 'pdf_text': <value>, 'object_key': <value>, 's3_url': <url>}]
        """
        return self.transformed_pdf_files

    async def extract_ruts_from_pdf(self, pdfs_data: list[dict]) -> list[dict]:
        tasks = []
        for pdf_data in pdfs_data:
            tasks.append(self._extract_ruts_from_pdf(pdf_data['pdf_text']))
        
        results = await asyncio.gather(*tasks)
        ruts = []
        
        for result in results:
            ruts.extend([rut.replace('.', '') for rut in result])
        
        ruts = list(set(ruts))
        ruts = [rut for rut in ruts if validate_rut(rut)]

        return ruts
    
    
    async def _extract_ruts_from_pdf(self, pdf_text: str) -> list[dict]:
        try:
            logger.info("Extracting RUTs from PDF", extra={"pdf_text": pdf_text})
            rut_pattern = r'\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]'
            mmatches = re.findall(rut_pattern, pdf_text)
            
            return mmatches
        except Exception as e:
            logger.error("Error extracting RUTs from PDF", extra={"error": str(e)})
            return []
    
    