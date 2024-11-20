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