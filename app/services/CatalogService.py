from app.libs.api import Catalog as CatalogAPI

class CatalogService:
    async def getCatlogs():
        params = "/open-api/product-images"
        response = await CatalogAPI.GET(params)

        return response