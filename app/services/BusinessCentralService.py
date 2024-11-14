from app.libs.api import BusinessCentral as BusinessCentralApi
from app.traits.BusinessCentralTraits import BusinessCentral as BusinessCentralTrait
from app.libs.helper import getDiscountPercentage, orderDateFormat
from app.settings.credentials import BusinessCentral as BusinessCentralCredentials

from datetime import datetime
from fastapi import HTTPException

class BusinessCentral:
    async def getAllProducts():
        token = await BusinessCentralApi.getBcToken()
        params = f"/Company('{BusinessCentralCredentials.company}')/Items"
        productsData = await BusinessCentralApi.odataGet(token, params)
        products = BusinessCentralTrait.processProducts(productsData)

        return products

    async def getProduct(number):
        token = await BusinessCentralApi.getBcToken()
        params = f"/Company('{BusinessCentralCredentials.company}')/workflowItems?$filter=number eq '"+number+"'"
        productsData = await BusinessCentralApi.odataGet(token, params)
        product = BusinessCentralTrait.processProductDetails(productsData)

        return product
    
    async def getDetailedProducts(number):
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/ItemDetails?$filter=No eq '"+number+"'"
        productsData = await BusinessCentralApi.odataGet(token, params)

        products = BusinessCentralTrait.processCompleteProductDetails(productsData)

        return products
    
    async def customers():
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/Customers"
        customerData = await BusinessCentralApi.odataGet(token, params)
        customers = BusinessCentralTrait.processCustomerData(customerData)

        return customers

    async def createSalesOrder(body):
        try:
            token = await BusinessCentralApi.getBcToken()
            params = f"companies({BusinessCentralCredentials.companyId})/salesOrders"
            headers = {}
            salesOrder = await BusinessCentralApi.apiPost(token, params, headers, body)

            return salesOrder
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong! Error: {str(e)}")

    async def getCompanies():
        token = await BusinessCentralApi.getBcToken()
        params = "companies"
        companies = await BusinessCentralApi.apiGet(token, params)

        return companies

    async def getUnitMeasurement(number):
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/ItemsUnitofMeasure?$filter=Item_No eq '"+number+"'"

        measurement_data = await BusinessCentralApi.odataGet(token, params)
        measurements = BusinessCentralTrait.processMeasurementData(measurement_data)

        return measurements
    
    async def getUnitMeasurements():
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/ItemsUnitofMeasure"
        measurements = await BusinessCentralApi.odataGet(token, params)

        return measurements

    async def getLocations():
        token = await BusinessCentralApi.getBcToken()
        params = f"companies({BusinessCentralCredentials.companyId})/locations"

        locations = await BusinessCentralApi.apiGet(token, params)

        return locations
    
    async def getLocation(code):
        token = await BusinessCentralApi.getBcToken()
        params = f"companies({BusinessCentralCredentials.companyId})/locations?$filter=code eq '{code}'"

        location = await BusinessCentralApi.apiGet(token, params)

        return BusinessCentralTrait.processLocationData(location)

    def processSalesLineItemRequest(product, shopifyOrderItem, shopifyOrder):
        return {
            "itemId": product["id"],
            "lineType": "Item",
            "lineObjectNumber": product["number"],
            "description": product["description"],
            "unitOfMeasureId": product["unitOfMeasureId"],
            "unitOfMeasureCode": product["baseUnitOfMeasure"],
            "quantity": float(shopifyOrderItem["quantity"]),
            "unitPrice": float(shopifyOrderItem['price']),
            "discountAmount": float(shopifyOrderItem['total_discount']),
            "discountPercent": getDiscountPercentage(shopifyOrderItem['price'], shopifyOrderItem['total_discount']),
            "shipmentDate": orderDateFormat(shopifyOrder["created_at"]),
            "invoiceQuantity": float(shopifyOrderItem["quantity"]),
            "shipQuantity": float(shopifyOrderItem["quantity"]),
        }

    async def createSalesOrderLines(body, orderId):
        try:
            token = await BusinessCentralApi.getBcToken()
            params = f"companies({BusinessCentralCredentials.companyId})/salesOrders("+orderId+")/salesOrderLines"
            headers = {}
            salesOrderLines = await BusinessCentralApi.apiPost(token, params, headers, body)

            return salesOrderLines
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Something went wrong! Error: {str(e)}")

    async def getProdRoutingLines():
        token = await BusinessCentralApi.getBcToken()
        params = f"/Company('{BusinessCentralCredentials.company}')/ProdOrderRoutingLines"
        prodRoutingLines = await BusinessCentralApi.odataGet(token, params)

        return prodRoutingLines

    async def getNexPageData(url):
        token = await BusinessCentralApi.getBcToken()
        prodRoutingLines = await BusinessCentralApi.odataGetNext(token, url)

        return prodRoutingLines
    
    async def getLedgerEntries(number):
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/Item_Ledger_Entries?$filter=Item_No eq '{number}'"

        entries = await BusinessCentralApi.odataGet(token, params)

        return entries
    
    async def getLatestPurchaseEntry(number):
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/Item_Ledger_Entries?$filter=Item_No eq '{number}' and Entry_Type eq 'Purchase'&top=1"

        entries = await BusinessCentralApi.odataGet(token, params)

        return entries

    async def getLatestConsumptionRecord(number, entry_number):
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/Item_Ledger_Entries?$filter=Item_No eq '{number}' and Entry_Type eq 'Consumption' and Entry_No gt {entry_number}"

        entries = await BusinessCentralApi.odataGet(token, params)

        return entries

    async def getAllLedgerEntries():
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/Item_Ledger_Entries"

        entries = await BusinessCentralApi.odataGet(token, params)

        return entries

    async def getProductQuantities():
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/ItemsAPI"

        entries = await BusinessCentralApi.odataGet(token, params)

        return entries

    async def processProductsQuantities(products, quantities):
        # Lists all products
        for product in products:
            product["quantity_on_hand"] = 0

            # Check if there is existing inventory
            for quanity in quantities["value"]:
                if product["number"] == quanity["US_APINo"]:
                    quanity_on_hand = (quanity["US_APIQtyHand"] - quanity["US_APIQtySales"])

                    if quanity_on_hand > 0:
                        product["quantity_on_hand"] = quanity_on_hand

        return products
    
    async def processProductMeasurements(products, measurements):
        # List all products
        for product in products:
            product["Height"] = 0
            product["Width"] = 0
            product["Length"] = 0
            product["Weight"] = 0

            for measurement in measurements["value"]:
                if product["number"] == measurement["Item_No"]:
                    product["Height"] = measurement["Height"]
                    product["Width"] = measurement["Width"]
                    product["Length"] = measurement["Length"]
                    product["Weight"] = measurement["Weight"]

        return products
    
    async def getCompleteProductDetails():
        token = await BusinessCentralApi.getBcToken()
        params = f"Company('{BusinessCentralCredentials.company}')/ItemDetails"

        productsData = await BusinessCentralApi.odataGet(token, params)
        products = BusinessCentralTrait.processCompleteProductDetails(productsData)

        return products