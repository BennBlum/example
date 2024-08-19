from pydantic import BaseModel, Field

class ExtractionRequest(BaseModel):
    data: str = Field(None, description="A base64 string representation of an image.")
    url: str = Field(None, description="The URL of the image.")