from pydantic import BaseModel
from datetime import datetime
from uuid import UUID, uuid4

class BaseDBModel(BaseModel):
    id: UUID = uuid4()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()