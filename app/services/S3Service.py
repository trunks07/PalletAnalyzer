from app.settings.credentials import S3 as S3Credentials

class S3Service:
    async def getFile(file_name):
        params = f"/{file_name}"
        endpoint = S3Credentials.endpoint

        url = endpoint+params

        return url