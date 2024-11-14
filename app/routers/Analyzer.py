from fastapi import FastAPI, APIRouter, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.services.OpenAIService import OpenAIzService

router = APIRouter()

@router.get("/chat", tags=["analyzer"])
async def chat(request: Request):
    try:
        message = await request.json()
        token = await OpenAIzService.client()
        response = await OpenAIzService(token, message["message"])

        status_code = status.HTTP_200_OK
        response = {"status": status_code, "data": response}
    except HTTPException  as e:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {"status": status_code, "error": e}

    print(response)

    return JSONResponse(status_code=status_code, content=response)