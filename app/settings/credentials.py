import os

from dotenv import load_dotenv
from app.settings.environment import Env as EnvSettings

if os.getenv("AWS_EXECUTION_ENV") is None:
    # Load environment variables from the .env file
    load_dotenv()

class Security:
    clientId = os.getenv("APP_CLIENT_ID")
    clientSecret = os.getenv("APP_CLIENT_SECRET")

class Openai:
    project_id = os.getenv("OPENAI_PROJECT_ID")
    organization = os.getenv("OPENAI_ORGANIZATIOM")
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

class BusinessCentral:
    if EnvSettings.environment == "sandbox":
        clientId = os.getenv("BC_TEST_CLIENT_ID")
        clientSecret = os.getenv("BC_TEST_CLIENT_SECRET")
        tokeEndPoint = os.getenv("BC_TEST_TOKEN_ENDPOINT")
        apiScopes = os.getenv("BC_TEST_API_SCOPES")
        odataEndPoint = os.getenv("BC_TEST_ODATA_ENDPOINT")
        apiEndPoint = os.getenv("BC_TEST_API_ENDPOINT")
        company = os.getenv("BC_TEST_COMPANY")
        companyId = os.getenv("BC_TEST_COMPANY_ID")
    else:
        clientId = os.getenv("BC_PROD_CLIENT_ID")
        clientSecret = os.getenv("BC_PROD_CLIENT_SECRET")
        tokeEndPoint = os.getenv("BC_PROD_TOKEN_ENDPOINT")
        apiScopes = os.getenv("BC_PROD_API_SCOPE")
        odataEndPoint = os.getenv("BC_PROD_ODATA_ENDPOINT")
        apiEndPoint = os.getenv("BC_PROD_API_ENDPOINT")
        company = os.getenv("BC_PROD_COMPANY")
        companyId = os.getenv("BC_PROD_COMPANY_ID")

    locationId = os.getenv("LOCATION_ID")
    CIAHandling = os.getenv("CIA_HANDLING")
    locationCode = os.getenv("LOCATION_CODE")
    walmartCustomer = os.getenv("WALMART_CUSTOMER")
    ebayCustomer = os.getenv("EBAY_CUSTOMER")
    overstocksCustomer = os.getenv("OVERSTOCKS_CUSTOMER")
    shopifyCustomer = os.getenv("SHOPIFY_CUSTOMER")
    CIACustomer = os.getenv("CIA_CUSTOMER")
    chargeItemId = os.getenv("CHARGE_ITEM_ID")
    chargeItemNumber = os.getenv("CHARGE_ITEM_NUMBER")

class Gemini:
    apiKey = os.getenv("GEMINI_API_KEY")
    endPoint = os.getenv("GEMINI_ENDPOINT")
    model = os.getenv("GEMINI_MODEL")
    baseUrl = os.getenv("GEMINI_BASE_URL")

class Catalog:
    endpoint = os.getenv("CATALOG_ENDPOINT")

class S3:
    endpoint = os.getenv("S3_ENDPOINT")