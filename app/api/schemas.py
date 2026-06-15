from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ClassifyRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class HandoffRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class HealthResponse(BaseModel):
    status: str
    service: str
    environment: str
