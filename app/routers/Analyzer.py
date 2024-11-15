import json

from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.services.OpenAIService import OpenAIzService
from app.services.BusinessCentralService import BusinessCentral as BusinessCentralService
from app.services.PalletService import PalletService
from app.services.GeminiService import GeminiService
from app.services.CatalogService import CatalogService

from app.libs.api import S3 as S3API

from app.traits.CatalogTraits import CatalogTrait

from app.libs.helper import convert_to_json

router = APIRouter()

@router.get("/chat", tags=["analyzer"])
async def chat(request: Request):
    try:
        request_data = await request.json()

        product_details = await BusinessCentralService.getDetailedProducts(request_data["sku"])
        measurement = await BusinessCentralService.getUnitMeasurement(request_data["sku"])

        if len(product_details) > 0:
            pallets = PalletService.list()
            message = f"This are my pallets {json.dumps(pallets)}, I have a product {product_details[0]["title"]} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided) and select the pallet to use, all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallent just return a json response."
            response = await GeminiService.completion(message)

            responses = []

            for data in response["candidates"]:
                if "content" in data:
                    content = data["content"]
                    if "parts" in content:
                        for part in content["parts"]:
                            if "text" in part:
                                print(part)
                                json_response = convert_to_json(part["text"])

                                responses.append(json_response)

            response = responses
        else:
            response = "Product Not Found!"

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.get("/analyze-image", tags=["analyzer"])
async def analyzeImage(request: Request):
    try:
        request_data = await request.json()

        product_details = await BusinessCentralService.getDetailedProducts(request_data["sku"])
        measurement = await BusinessCentralService.getUnitMeasurement(request_data["sku"])

        if len(product_details) > 0:
            catalogs = await CatalogService.getCatlogs()
            file = await CatalogTrait.getFile(catalogs, request_data["sku"])

            downloaded = await S3API.downloadImage(file["url"])
            upload_url = await GeminiService.getUploadURL(file["title"], downloaded)

            file_url = await GeminiService.uploadImage(downloaded["num_bytes"], downloaded["image_data"], upload_url)

            pallets = PalletService.list()
            message = f"This are my pallets {json.dumps(pallets)}, I have a product {product_details[0]["title"]} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided. Refer to the attached image for better visualization so you will be able to know where to devide the product) and select the pallet to use for the product or for each parts of the product (if disassembled), all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallet remember that is it is one is to one meaning each part is one pallet if it can fit on a single pallet that is better just return a response in complete json format including the comments on the solution."
            
            response = await GeminiService.imageCompletion(message, file_url)
        else:
            response = "Product Not Found!"

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)