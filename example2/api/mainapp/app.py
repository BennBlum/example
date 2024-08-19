import requests
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from mainapp.factory import Factory
from mainapp.utilities.image_utils import base64str_to_image, bytes_to_image
from mainapp.schemas.extraction_request import ExtractionRequest
from mainapp.schemas.extraction_response import ExtractionResponse

load_dotenv()

app = FastAPI()
factory = Factory()

@app.get("/")
async def index():
    return {"version": os.getenv("VERSION")}

@app.post("/extract")
async def extract(
    request_body: ExtractionRequest, 
    auth_key: str = Header(None), 
    auth_service = Depends(factory.create_auth_service),
    passport_extraction_service = Depends(factory.create_passport_service)
) -> ExtractionResponse:
    auth_service.authorize(auth_key)    
    image_data = request_body.data
    url = request_body.url

    if image_data is not None:
        image = base64str_to_image(image_data=image_data)
    elif url is not None:
        try:
            response = requests.get(url)
            response.raise_for_status()
            image = bytes_to_image(response.content)
        except requests.RequestException as e:
            raise HTTPException(status_code=400, detail="Invalid URL or unable to fetch image")

    extraction_result = passport_extraction_service.process(image)
    return ExtractionResponse(result=extraction_result)