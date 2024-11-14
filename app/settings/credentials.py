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
    secret_key = os.getenv("OPENAI_SECRET_KEY")

class BusinessCentral:
    if EnvSettings.environment == "sandbox":
        clientId = "c339a828-b6a5-404d-bf4c-395cb7638170"
        clientSecret = "3GV8Q~LEgs8TYXfNCO2gY2Q~KnJI_SewNuipuaHD"
        tokeEndPoint = "https://login.microsoftonline.com/c53514c2-3d4e-4768-b750-aa47f09d8a44/oauth2/v2.0/token"
        apiScopes = "https://api.businesscentral.dynamics.com/.default"
        odataEndPoint = "https://api.businesscentral.dynamics.com/v2.0/c53514c2-3d4e-4768-b750-aa47f09d8a44/MKTADEVCOPY/ODataV4/"
        apiEndPoint = "https://api.businesscentral.dynamics.com/v2.0/MKTADEVCOPY/api/v2.0/"
        company = 'MKTA%20Philippines%2C%20Inc.'
        companyId = "69b5dc62-dc9a-ed11-bff5-6045bd1c4457"
    else:
        clientId = "6014c9b5-38b1-4606-b0ba-7c61d377116d"
        clientSecret = "TLo8Q~_qFL6dcB.mz2ZfZOcI6F3v-FI55O8fYbAw"
        tokeEndPoint = "https://login.microsoftonline.com/acf2f8ef-17f3-44b9-a8e9-6347a87e36e0/oauth2/v2.0/token"
        apiScopes = "https://api.businesscentral.dynamics.com/.default"
        odataEndPoint = "https://api.businesscentral.dynamics.com/v2.0/acf2f8ef-17f3-44b9-a8e9-6347a87e36e0/Production/ODataV4/"
        apiEndPoint = "https://api.businesscentral.dynamics.com/v2.0/Production/api/v2.0/"
        company = 'Universal%20Statues'
        companyId = "eeba6bd7-b192-ed11-bff5-6045bda9ddfd"

    locationId = "b6cab00a-922d-ee11-bdf5-000d3a12c491"
    CIAHandling = "IC_HANDLING"
    locationCode = "MEMPHIS"
    walmartCustomer = "CUST000414"
    ebayCustomer = "CUST000392"
    overstocksCustomer = "CUST000379"
    shopifyCustomer = "CUST000447"
    CIACustomer = "CUST000198"
    chargeItemId = "1390fea1-b4f8-ee11-a200-000d3a9e34a3"
    chargeItemNumber = "SALES FERIGHT"