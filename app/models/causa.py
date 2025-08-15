from pydantic import BaseModel

class CausaItem(BaseModel):
    causa_id: str
    #litigantes: list[dict]
    #pdf_paths: list[dict]