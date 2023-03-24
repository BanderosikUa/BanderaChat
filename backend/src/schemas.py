from pydantic import BaseModel, Field

from typing import List

# class Error(BaseModel):
#     error: dict = Field(..., example={"email": "Email is already taken."})


class ErrorResponse(BaseModel):
    status: str = "error"
    detail: List[dict] = Field(..., example=[{"email": "Email is already taken."}])
