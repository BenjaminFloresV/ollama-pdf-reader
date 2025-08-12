from pydantic import BaseModel

class CausaItem(BaseModel):
    causa_id: int
    #litigantes: list[dict]
    #pdf_paths: list[dict]