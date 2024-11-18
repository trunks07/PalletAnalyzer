import asyncio
import uvicorn

from fastapi.responses import JSONResponse
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import Depends, FastAPI, Request, status
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers import Analyzer, System, Catalog
from app.settings.environment import Env
from app.settings.credentials import Security
from app.services.EmailService import EmailService
from app.routers.middleware.SecurityMiddleware import SecurityMiddleware

from mangum import Mangum

# Main OverstocksAPI application
app = FastAPI()

asgi_handler = Mangum(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow all origins (change to a specific list if needed)
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

def lambda_handler(event, context):
    # For API Gateway events, return using Mangum
    return asgi_handler(event, context)

# Global handler for HTTP exceptions (e.g., 400, 404, etc.)
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    subject = f"HTTP Error - Status Code: {exc.status_code}"
    body = f"An HTTP error occurred:\n\nStatus: {exc.status_code}\nDetail: {exc.detail}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "detail": exc.detail}
    )

# Global handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    subject = "Validation Error in OverstocksAPI - Status Code: 422"
    body = f"Validation Error:\n\nErrors: {exc.errors()}\nBody: {exc.body}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": status.HTTP_422_UNPROCESSABLE_ENTITY, "detail": exc.errors()}
    )

# Catch-all handler for unhandled exceptions
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    subject = f"Unhandled Error in OverstocksAPI - {type(exc).__name__}"
    body = f"An unhandled error occurred:\n\nException Type: {type(exc).__name__}\nDetail: {str(exc)}\n"
    recipient_email = Env.admin_email
    # Send Email to the administrator
    await EmailService.send_error_email(subject, body, recipient_email)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": status.HTTP_500_INTERNAL_SERVER_ERROR, "detail": "An internal server error occurred"}
    )

app.include_router(System.router)
app.add_middleware(GZipMiddleware)

analyzer_app = FastAPI()
analyzer_app.include_router(Analyzer.router)
analyzer_app.add_middleware(
    SecurityMiddleware,
    expected_clientId=Security.clientId,
    expected_clientSecret=Security.clientSecret
)
analyzer_app.add_middleware(GZipMiddleware)

catalog_app = FastAPI()
catalog_app.include_router(Catalog.router)
catalog_app.add_middleware(
    SecurityMiddleware,
    expected_clientId=Security.clientId,
    expected_clientSecret=Security.clientSecret
)
catalog_app.add_middleware(GZipMiddleware)

app.mount('/analyzer', analyzer_app)
app.mount('/catalogs', catalog_app)

# Local server setup for testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)