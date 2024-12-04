from app.libs.api import Catalog as CatalogAPI
from app.settings.credentials import Catalog as CatalogCredentials

class CatalogService:
    async def getCatlogs():
        params = f"/product-images?passPhrase={CatalogCredentials.passPhrase}"

        response = await CatalogAPI.GET(params)

        return response