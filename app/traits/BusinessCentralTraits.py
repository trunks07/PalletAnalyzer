import json

class BusinessCentral:
    def processProducts(productsData):
        products = []

        for product in productsData["value"]:
            products.append({
                "number": product["No"],
                "title": product["Description"].title(),
                "description": product["Description"].title(),
                "unit_cost": product["Unit_Cost"],
                "unit_of_measure": product["Base_Unit_of_Measure"],
                "category": product["Item_Category_Code"].title(),
                "group": product["Gen_Prod_Posting_Group"].title(),
                "updated_at": product["Last_Date_Modified"],
                "vendor": product["Vendor_No"]
            })

        return products
    
    def processCompleteProductDetails(productsData):
        products = []

        for product in productsData["value"]:
            products.append({
                "number": product["No"],
                "title": product["Description"].title(),
                "description": product["Description"].title(),
                "unit_cost": product["Unit_Cost"],
                "unit_price": product["Unit_Price"],
                "unit_of_measure": product["Base_Unit_of_Measure"],
                "category": product["Item_Category_Code"].title(),
                "group": product["Gen_Prod_Posting_Group"].title(),
                "updated_at": product["Last_Date_Modified"],
                "ShopifyPrice": (product["ShopifyPrice"] if "ShopifyPrice" in product else 0),
                "eBayPrice": (product["eBayPrice"] if "ShopifyPrice" in product else 0),
                "WalmartPrice": (product["WalmartPrice"] if "ShopifyPrice" in product else 0),
                "BBnBPrice": (product["BBnBPrice"] if "ShopifyPrice" in product else 0)
            })

        return products

    def processLocationData(locationData):
        if "value" in locationData:
            location = locationData["value"][0]

            return {
                "id": location["id"],
                "code": location["code"],
            }

    def processProductDetails(productData):
        if(productData["value"]):
            return productData["value"][0]
        else:
            return {}

    def processCustomerData(customerData):
        if(customerData["value"]):
            return customerData["value"]
        else:
            return {}

    def processOrderRoutingData(routing_lines, data = []):
        for rounting_line in routing_lines["value"]:
            data.append({
                "Routing_No": rounting_line["Routing_No"],
                "Type": rounting_line["Type"],
                "Routing_Link_Code": rounting_line["Routing_Link_Code"],
                "Operation_No": rounting_line["Operation_No"],
                "Concurrent_Capacities": rounting_line["Concurrent_Capacities"],
                "Run_Time": rounting_line["Run_Time"],
            })

        return data
    
    def processBoMLinesData(bom_lines, data = []):
        for bom_line in bom_lines["value"]:
            data.append({
                "Production_BOM_No": bom_line["Production_BOM_No"],
                "No": bom_line["No"],
                "Quantity_per": bom_line["Quantity_per"],
                "Unit_of_Measure_Code": bom_line["Unit_of_Measure_Code"],
                "Routing_Link_Code": bom_line["Routing_Link_Code"],
            })

        return data
    
    async def processStreamBoMLinesData(bom_lines):
        for bom_line in bom_lines["value"]:
            line_data = {
                "Production_BOM_No": bom_line["Production_BOM_No"],
                "No": bom_line["No"],
                "Quantity_per": bom_line["Quantity_per"],
                "Unit_of_Measure_Code": bom_line["Unit_of_Measure_Code"],
                "Routing_Link_Code": bom_line["Routing_Link_Code"],
            }
            # Yield as JSON string with newline for each item
            yield json.dumps(line_data) + ",\n"
    
    def processItemListsData(item_lists, data = []):
        for item_list in item_lists["value"]:
            data.append({
                "No": item_list["No"],
                "Description": item_list["Description"],
                "Base_Unit_of_Measure": item_list["Base_Unit_of_Measure"],
                "Production_BOM_No": item_list["Production_BOM_No"],
                "Routing_No": item_list["Routing_No"],
                "Replenishment_System": item_list["Replenishment_System"],
                "Gen_Prod_Posting_Group": item_list["Gen_Prod_Posting_Group"]
            })

        return data

    def processDimensionsData(routing_lines, data = []):
        for rounting_line in routing_lines["value"]:
            data.append({
                "Code": rounting_line["Code"],
                "Item_No": rounting_line["Item_No"],
                "Height": rounting_line["Height"],
                "Width": rounting_line["Width"],
                "Length": rounting_line["Length"],
                "Cubage": rounting_line["Cubage"],
                "Weight": rounting_line["Weight"]
            })

        return data
    
    def processWorkCentersData(routing_lines, data = []):
        for rounting_line in routing_lines["value"]:
            data.append({
                "Work_Center_Group_Code": rounting_line["Work_Center_Group_Code"],
                "No": rounting_line["No"],
                "Name": rounting_line["Name"]
            })

        return data
    
    def processLedgerEntryData(ledger_entries):
        data = []

        for leder_entry in ledger_entries["value"]:
            data.append({
                "Entry_Type": leder_entry["Entry_Type"],
                "Entry_No": leder_entry["Entry_No"],
                "Item_No": leder_entry["Item_No"],
                "Quantity": leder_entry["Quantity"],
                "Remaining_Quantity": leder_entry["Remaining_Quantity"],
                "Posting_Date": leder_entry["Posting_Date"]
            })

        return data
    
    def appendAddtionalData(data, array = []):
        for datum in data:
            array.append(datum)

        return array
    
    def processMeasurementData(data):
        measurement = data["value"][0]
        return {
            "sku": measurement["Item_No"],
            "height": measurement["Height"],
            "width": measurement["Width"],
            "length": measurement["Length"],
            "cubage": measurement["Cubage"],
            "weight": measurement["Weight"]
        }