import aiohttp
import mimetypes
import json

from app.settings.credentials import Gemini as GeminiCredentials
from app.libs.api import Gemini as GeminiApi

from app.libs.helper import convert_to_json

class GeminiService:
    async def completion(message):
        params = f":generateContent?key={GeminiCredentials.apiKey}"
        body = {
            "contents": [{
                "parts": [{
                    "text": message
                }]
            }]
        }

        headers = {}

        response = await GeminiApi.POST(params, headers, body)

        return response
    
    async def getUploadURL(title, downloaded):
        metadata = {
            'file': {
                'display_name': title
            }
        }

        headers = {
            "X-Goog-Upload-Protocol": "resumable",
            "X-Goog-Upload-Command": "start",
            "X-Goog-Upload-Header-Content-Length": str(downloaded["num_bytes"]),
            "X-Goog-Upload-Header-Content-Type": downloaded["mime_type"],
            "Content-Type": "application/json"
        }

        upload_url = await GeminiApi.getUploadURL(
            GeminiCredentials.apiKey,
            headers,
            metadata
        )

        return upload_url

    async def imageCompletion(message, file_uri):
        generate_data = {
            "contents": [
                {
                    "parts": [
                        {"text": message},
                        {
                            "file_data": {
                                "mime_type": "image/jpeg",
                                "file_uri": file_uri
                            }
                        }
                    ]
                }
            ]
        }

        headers = {
            "Content-Type": "application/json"
        }

        params = f":generateContent?key={GeminiCredentials.apiKey}"

        response_data = await GeminiApi.POST(params, headers, generate_data)

        responses = []

        # Extract and print the generated content
        candidates = response_data.get("candidates", [])
        for candidate in candidates:
            parts = candidate.get("content", {}).get("parts", [])
            for part in parts:
                text = part.get("text", "")
                json_response = convert_to_json(part["text"])
                responses.append(json_response)

        return responses
    

    async def uploadImage(num_bytes, image_data, upload_url):
        headers = {
            "Content-Length": str(num_bytes),
            "X-Goog-Upload-Offset": "0",
            "X-Goog-Upload-Command": "upload, finalize"
        }

        file_uri = await GeminiApi.uploadImage(upload_url, headers, image_data)

        return file_uri