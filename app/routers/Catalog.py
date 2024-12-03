import json

from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.services.CatalogService import CatalogService
from app.services.BusinessCentralService import BusinessCentral as BusinessCentralService

router = APIRouter()

@router.get("/get-catalogs", tags=["catalogs"])
async def getCatalogs():
    try:
        catalogs = await CatalogService.getCatlogs()

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": catalogs}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.get("/get-products", tags=["catalogs"])
async def getCatalogs():
    try:
        products = await BusinessCentralService.getAllProducts()

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": products}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)

@router.get("/get-available-products")
async def getAvailableProducts():
    try:
        available_products = []
        existing_products = set()  # Use a set for efficient lookup

        catalogs = await CatalogService.getCatlogs()
        products = await BusinessCentralService.getAllProducts()

        # Create a set of catalog product IDs for quick lookup
        catalog_product_ids = {catalog["product_id"] for catalog in catalogs}

        for product in products:
            product_number = product["number"]
            if product_number in catalog_product_ids and product_number not in existing_products:
                available_products.append(product)
                existing_products.add(product_number)  # Track processed product numbers

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": available_products}

    except HTTPException as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": str(e)}  # Convert error to string

    return JSONResponse(status_code=status_code, content=response)

@router.post("/get-filtered-products", tags=["catalogs"])
async def getCatalogs(request: Request):
    try:
        request = await request.json()
        product_array = request["ids"]

        products = await BusinessCentralService.getProductLists(product_array)

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": products}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    return JSONResponse(status_code=status_code, content=response)