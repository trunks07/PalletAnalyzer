from app.services.S3Service import S3Service

class CatalogTrait:
    async def getFile(catalogs, sku):
        for catalog in catalogs:
            if catalog["product_id"] == sku:
                return {
                    "url": await S3Service.getFile(f"thumbs/{catalog["file"]["filename"]}"),
                    "title": catalog["file"]["title"]
                }