from pydantic import BaseModel
from datetime import datetime

class DocumentResponse(BaseModel):
    filename: str
    uploaded_by: str
    uploaded_at: datetime
    status: str