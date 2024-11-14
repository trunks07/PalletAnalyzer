from openai import OpenAI
from app.settings.credentials import Openai

client = OpenAI(
    organization = Openai.organization,
    project = Openai.project_id,
)

class OpenAIzService:
    async def completion(message):
        completion = client.chat.completions.create(
        model = Openai.model,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        return completion