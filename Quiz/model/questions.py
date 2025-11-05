from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from bson import ObjectId

class Question(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")    
    text: str
    alternatives: List[Dict[str, str]]  # espera {"id": "...", "text": "..."}
    correct_answer_id: int

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
