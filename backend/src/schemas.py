from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass

from typing import Optional, List

# class Error(BaseModel):
#     error: dict = Field(..., example={"email": "Email is already taken."})


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: List[dict] = Field(
        ..., example=[{"email": "Email is already taken."}]
        )


class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 10
    

class AllOptional(ModelMetaclass):
    def __new__(self, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            annotations.update(base.__annotations__)
        for field in annotations:
            if not field.startswith('__'):
                annotations[field] = Optional[annotations[field]]
        namespaces['__annotations__'] = annotations
        return super().__new__(self, name, bases, namespaces, **kwargs)
