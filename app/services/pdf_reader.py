from app.services.base import BaseService
from app.utils.pdf import load_pdf


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

    async def extract_ruts_from_pdf(self, pdf_bytes: bytes) -> list[dict]:
        # TODO: Implement regex extraction of ruts from pdf text and then pass that RUT to the rutificador service
        pass
    
    
    
    
    