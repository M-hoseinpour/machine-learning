import requests
import time
import csv

# @params
api_url = "https://www.sheypoor.com/api/v10.0.0/search/iran/houses-apartments-for-sale"
number_of_requests = 4880  # Number of pages you want to fetch (24 item per page)
page = 1
last_item_page_id = None
headers = {
    'User-Agent': 'PostmanRuntime/7.32.2',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}
columns = ['id',
            'type',
            "title",
            "location",
            "age",
            "elevator",
            "parking",
            "type_of_document",
            "rooms",
            "area_meterage",
            "number_of_units_per_floor",
            "number_floor",
            "heating_and_cooling_system",
            "meterage",
            "cabinets",
            "building_facades",
            "floor_covering",
            "kitchen",
            "year_of_building",
            "warehouse",
            "property_floor",
            "property_type",
            "lat",
            "lon",
            "price"
            ]

output_file = "price-prediction.csv"

def find_attribute_by_id(data_list, target_id, attribute):
    for item in data_list:
        if item['id'] == target_id:
            return item.get(attribute, "null")
    return 'null'

def write_to_file(data):
    fullAttributes = data.get("fullAttributes", {})
    price_list = data.get('attributes', {}).get('price', [])
    writer.writerow([
        data.get('id', 'null'),
        data.get('type', 'null'),
        data.get('attributes', {}).get('title', "null"),
        data.get("attributes", {}).get("location", 'null'),
        find_attribute_by_id(fullAttributes, "69188", "value"), # age,
        find_attribute_by_id(fullAttributes, "69194", "value"), # elevator
        find_attribute_by_id(fullAttributes, "69190", "value"), # parking
        find_attribute_by_id(fullAttributes, "69232", "value"), # type of Document
        find_attribute_by_id(fullAttributes, "68133", "value"), # rooms
        find_attribute_by_id(fullAttributes, "69237", "value"), # area meterage
        find_attribute_by_id(fullAttributes, "69222", "value"), # number of units per floor
        find_attribute_by_id(fullAttributes, "69217", "value"), # number of floors
        find_attribute_by_id(fullAttributes, "95004", "value"), # heating and cooling system
        find_attribute_by_id(fullAttributes, "68085", "value"), # meterage
        find_attribute_by_id(fullAttributes, "95002", "value"), # cabinets
        find_attribute_by_id(fullAttributes, "95000", "value"), # building facades
        find_attribute_by_id(fullAttributes, "95003", "value"), # floor covering
        find_attribute_by_id(fullAttributes, "95001", "value"), # kitchen
        find_attribute_by_id(fullAttributes, "92368", "value"), # year of building
        find_attribute_by_id(fullAttributes, "69192", "value"), # warehouse
        find_attribute_by_id(fullAttributes, "94550", "value"), # property floor
        find_attribute_by_id(fullAttributes, "68094", "value"), # property type
        data.get("geo", {}).get("lat", 'null'),
        data.get("geo", {}).get("lon", 'null'),
        price_list[0].get("amount", 'null') if price_list else 'null'
        ])

# Write headers to the CSV (only once at the start)
with open(output_file, 'w', newline='',  encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(columns)  

for page in range(1, number_of_requests + 1):
    params = {
        'p': page,
        'f': last_item_page_id 
    }
    
    try:
        response = requests.get(api_url, params=params,  headers=headers)
        response.raise_for_status()

        data = response.json()
        houses = data["data"]
        last_item_page_id = data["meta"]["f"]

        with open(output_file, 'a', newline='',  encoding='utf-8') as f:
            writer = csv.writer(f)
            for house in houses:
                if house.get("type", "") == 'vip':
                    items = house.get("items", [])
                    for item in items:
                        write_to_file(item)
                else:
                     write_to_file(house)
             
        # Pause for a short time to avoid rate limits
        time.sleep(1)

    except requests.exceptions.RequestException as err:
        print("Error:", err)
        time.sleep(10)  # Sleep and try again
    # progress
    progress = page / number_of_requests * 100
    print("Page: {} {:.2f}%".format(page, round(progress, 2)))  

