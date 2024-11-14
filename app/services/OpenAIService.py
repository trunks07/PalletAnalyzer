from openai import OpenAI
from app.settings.credentials import Openai

class OpenAIzService:
    async def client():
        client = OpenAI(
            organization=Openai.organization,
            project=Openai.project_id,
        )

        return client

    async def completion(client, message):
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return completion