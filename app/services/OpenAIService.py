import requests
import base64

from openai import OpenAI
from app.settings.credentials import Openai as OpenAICredentials

client = OpenAI(
    organization = OpenAICredentials.organization,
    project = OpenAICredentials.project_id,
)

class OpenAIzService:
    async def completion(message):
        completion = client.chat.completions.create(
        model = OpenAICredentials.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return completion
    
    async def imageCompletion(message, image):
        request_response = requests.get(image)
        image_base64 = base64.b64encode(request_response.content).decode("utf-8")
        response = client.chat.completions.create(
            model = OpenAICredentials.model,
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": message},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}",
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        return response.choices[0].message.content