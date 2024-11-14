import aiohttp

from app.settings.credentials import Gemini as GeminiCredentials
from app.libs.api import Gemini as GeminiApi

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