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

from app.libs.helper import convert_to_json, process_json_response

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

@router.post("/analyze-image", tags=["analyzer"])
async def analyzeImage(request: Request):
    try:
        request_data = await request.json()

        product_name = request_data["name"]
        sku = request_data["sku"]

        measurement = await BusinessCentralService.getUnitMeasurement(sku)

        if len(measurement) > 0:
            catalogs = await CatalogService.getCatlogs()
            file = await CatalogTrait.getFile(catalogs, sku)

            if file:
                downloaded = await S3API.downloadImage(file["url"])
                upload_url = await GeminiService.getUploadURL(file["title"], downloaded)

                file_url = await GeminiService.uploadImage(downloaded["num_bytes"], downloaded["image_data"], upload_url)

                pallets = PalletService.list()
                jsonFormat = PalletService.jsonFormat()

                message = f"This are my pallets {json.dumps(pallets)} (Please use the standard one as much as possible), I have a product {product_name} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided. Refer to the attached image for better visualization so you will be able to know where to devide the product) and select the pallet to use for the product or for each parts of the product (if disassembled), all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallet remember that is it is one is to one meaning each part is one pallet if it can fit on a single pallet that is better just return a response in using this json format {json.dumps(jsonFormat)} do not add any other answer outside of this json format the whole answer should be this format."

                response = await GeminiService.imageCompletion(message, file_url)
            else:
                response = "Product catalog not found"
        else:
            response = "Product Not Found!"

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.post("/bulk-analyze-image")
async def bulkAnalyzeImage(request: Request):
    try:
        analysis = []
        request_data = await request.json()
        items = request_data["items"]

        for item in items:
            product_name = item["name"]
            sku = item["sku"]

            measurement = await BusinessCentralService.getUnitMeasurement(sku)

            if len(measurement) > 0:
                catalogs = await CatalogService.getCatlogs()
                file = await CatalogTrait.getFile(catalogs, sku)

                if file:
                    downloaded = await S3API.downloadImage(file["url"])
                    upload_url = await GeminiService.getUploadURL(file["title"], downloaded)

                    file_url = await GeminiService.uploadImage(downloaded["num_bytes"], downloaded["image_data"], upload_url)

                    pallets = PalletService.list()
                    jsonFormat = PalletService.jsonFormat()

                    message = f"This are my pallets {json.dumps(pallets)} (Please use the standard one as much as possible), I have a product {product_name} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided. Refer to the attached image for better visualization so you will be able to know where to devide the product) and select the pallet to use for the product or for each parts of the product (if disassembled), all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallet remember that is it is one is to one meaning each part is one pallet if it can fit on a single pallet that is better just return a response in using this json format {json.dumps(jsonFormat)} do not add any other answer outside of this json format the whole answer should be this format."

                    response = await GeminiService.imageCompletion(message, file_url)

                    analysis.append({"response": response, "title": product_name})
                else:
                    response = "Product catalog not found"
            else:
                response = "Product Not Found!"

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": analysis}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.post("/gpt-image-analyzer")
async def gptImageAnalyzer(request: Request):
    try:
        request_data = await request.json()

        product_name = request_data["name"]
        sku = request_data["sku"]

        measurement = await BusinessCentralService.getUnitMeasurement(sku)

        if len(measurement) > 0:
            catalogs = await CatalogService.getCatlogs()
            file = await CatalogTrait.getFile(catalogs, sku)

            if file:
                image_url = file["url"]

                pallets = PalletService.list()
                jsonFormat = PalletService.jsonFormat()

                message = f"This are my pallets {json.dumps(pallets)} (Please use the standard one as much as possible), I have a product {product_name} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided. Refer to the attached image for better visualization so you will be able to know where to devide the product) and select the pallet to use for the product or for each parts of the product (if disassembled), all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallet remember that is it is one is to one meaning each part is one pallet if it can fit on a single pallet that is better just return a response in using this json format {json.dumps(jsonFormat)} do not add any other answer outside of this json format the whole answer should be this format."

                image_response = await OpenAIzService.imageCompletion(message, image_url)

                response = process_json_response(image_response)
            else:
                response = "Product catalog not found"
        else:
            response = "Product Not Found!"

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.post("/bulk-gpt-image-analyzer")
async def bulkAnalyzeImage(request: Request):
    try:
        request_data = await request.json()
        items = request_data["items"]

        query = []
        for item in items:
            product_name = item["name"]
            sku = item["sku"]

            measurement = await BusinessCentralService.getUnitMeasurement(sku)

            if len(measurement) > 0:
                catalogs = await CatalogService.getCatlogs()
                file = await CatalogTrait.getFile(catalogs, sku)

                if file:
                    image_url = file["url"]

                    pallets = PalletService.list()
                    jsonFormat = PalletService.jsonFormat()

                    message = f"This are my pallets {json.dumps(pallets)} (Please use the standard one as much as possible), I have a product {product_name} with dimension {json.dumps(measurement)}. Now from that can you select the most suitable pallet to use or disassemble the product into several pieces if needed (You can do the estimation how many fragments should the product be disassembled to fit in the pallets but please cosider the product assembly and divide it accordingly (Head, Arm, Leg) if applicable. its all up to you how you want it to be divided. Refer to the attached image for better visualization so you will be able to know where to devide the product) and select the pallet to use for the product or for each parts of the product (if disassembled), all the measurement I used were in inches. Then from that give us the pallets will be used which part is going to that pallet remember that is it is one is to one meaning each part is one pallet if it can fit on a single pallet that is better just return a response in using this json format {json.dumps(jsonFormat)} do not add any other answer outside of this json format the whole answer should be this format."

                    query.append({
                        "is_found": True,
                        "message": message,
                        "image_url": image_url
                    })
                else:
                    query.append({
                        "is_found": False,
                        "message": "Product catalog not found"
                    })
            else:
                query.append({
                    "is_found": False,
                    "message": "Product Not Found!"
                })

        analysis_responses = await OpenAIzService.bulkImageCompletion(query)

        analysis = []
        for analysis_response in analysis_responses:
            analysis.append(process_json_response(analysis_response))

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": analysis}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)