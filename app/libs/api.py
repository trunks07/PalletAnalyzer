import os
import json
import aiohttp
import binascii
import mimetypes

import xml.etree.ElementTree as ET1

from app.settings.credentials import Gemini as GeminiCredentials
from app.settings.credentials import BusinessCentral as BusinesCentralCrendentials
from app.settings.credentials import Catalog as CatalogCredentials
from app.settings.credentials import S3 as S3Credentials
from app.libs.helper import get_basic_auth_header,  generate_correlation_id, xml_to_dict, xml_to_json

class BusinessCentral:
    async def getBcToken():
        clientId = BusinesCentralCrendentials.clientId
        clientSecret = BusinesCentralCrendentials.clientSecret
        tokenEndpoint = BusinesCentralCrendentials.tokeEndPoint

        scope = BusinesCentralCrendentials.apiScopes

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            'grant_type': 'client_credentials',
            'client_id': clientId,
            'client_secret': clientSecret,
            'scope': scope,  # Optionally, specify the required scope
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(tokenEndpoint, data=data, headers=headers) as resp:
                token = await resp.json()

        return token

    async def odataGet(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def odataGetNext(token, url, headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        async with aiohttp.ClientSession() as session:
            async with session.get(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def odataPost(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def odataPut(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def odataPatch(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def odataPut(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def odataDelete(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.odataEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, data=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def apiGet(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def apiPost(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def apiPut(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def apiPatch(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response

    async def apiPut(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response
    
    async def apiDelete(token, params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = 'Bearer ' + token["access_token"]

        apiEndPoint = BusinesCentralCrendentials.apiEndPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=body, headers=headers) as resp:
                response = await resp.json()

        return response

class Gemini:
    async def GET(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = GeminiCredentials.endPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def POST(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = GeminiCredentials.endPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def PUT(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = GeminiCredentials.endPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def PATCH(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = GeminiCredentials.endPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def DELETE(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = GeminiCredentials.endPoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def getUploadURL(token, headers, metadata):
        base_url = GeminiCredentials.baseUrl
        init_url = f"{base_url}/upload/v1beta/files?key={token}"

        async with aiohttp.ClientSession() as session:
            async with session.post(init_url, headers=headers, json=metadata) as init_response:
                init_response.raise_for_status()
                upload_url = init_response.headers.get("X-Goog-Upload-URL")

            if not upload_url:
                raise Exception("Failed to get upload URL.")
            else:
                return upload_url

    async def uploadImage(upload_url, headers, image_data):
        async with aiohttp.ClientSession() as session:
            async with session.post(upload_url, headers=headers, data=image_data) as upload_response:
                upload_response.raise_for_status()
                file_info = await upload_response.json()

            file_uri = file_info.get("file", {}).get("uri")
            if not file_uri:
                raise Exception("Failed to retrieve file URI.")
            else:
                return file_uri

class Catalog:
    async def GET(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = CatalogCredentials.endpoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.get(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def POST(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = CatalogCredentials.endpoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def PUT(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = CatalogCredentials.endpoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def PATCH(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = CatalogCredentials.endpoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response
    
    async def DELETE(params="", headers={}, body={}):
        headers["Content-Type"] = "application/json"

        apiEndPoint = CatalogCredentials.endpoint
        url = apiEndPoint+params

        async with aiohttp.ClientSession() as session:
            async with session.delete(url, json=body, headers=headers) as resp:

                response = await resp.json()

        return response

class S3:
    async def downloadImage(s3_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(s3_url) as s3_response:
                s3_response.raise_for_status()
                image_data = await s3_response.read()
                mime_type, _ = mimetypes.guess_type(s3_url)
                mime_type = mime_type or "application/octet-stream"
                num_bytes = len(image_data)

        return {
            "image_data": image_data,
            "mime_type": mime_type,
            "num_bytes": num_bytes
        }