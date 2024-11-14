import os
import json
import aiohttp
import binascii

import xml.etree.ElementTree as ET1

from app.settings.credentials import Gemini as GeminiCredentials
from app.settings.credentials import BusinessCentral as BusinesCentralCrendentials
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