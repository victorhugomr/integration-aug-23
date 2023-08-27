import csv
import json
import os
import requests
from datetime import datetime

def send_product_to_api(products):
    # API configuration
    BASE_URL = "https://api.instabuy.com.br/store/"
    ENDPOINT = "products"
    API_KEY = "Mq1EWAXiHwraLIQgfq4stmUxKiM6VpC5Xd9o3wuX1Go"

    headers = {
        "api-key": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    response = requests.put(f"{BASE_URL}{ENDPOINT}", headers=headers, params = products)
    return response

def file_in_same_directory(file_name):
   script_dir = os.path.dirname(os.path.abspath(__file__))
   file_path = os.path.join(script_dir, file_name)
   return file_path

def datetime_to_iso(date_str):
    if(len(date_str) == 46 and date_str[37]=='T'):
        start_date, end_date = date_str.split('/')
        return datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%f')
    if(date_str == ""):
        return ""
    months = {
        "JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
        "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12
    }
    day, abb_month, year = date_str.split('-')
    day = int(day)
    month = months[abb_month]
    if(day>31 or month>12):
        return ""
    if(day>29 and month==2):
        return ""
    year = int(year) + 2000
    hour, minute, second = 0, 0, 0
    f = 672000
    date_iso = str(year)+'-'+str(month)+'-'+str(day)+'T'+str(hour)+':'+str(minute)+':'+str(second)+'.'+str(f)
    return datetime.strptime(date_iso, '%Y-%m-%dT%H:%M:%S.%f')

def csv_to_json():
    #Read CSV and add data to a dictionary
    with open(file_in_same_directory('items.csv'), encoding="utf8") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=';')
        data_list = list()
        for csvRow in csvReader:
            data_list.append(csvRow)

    data_list.pop(0)
    #Converting string to other types in list
    for properties in data_list:
        properties[3] = properties[3].replace(',', '.')
        properties[3] = float(properties[3])
        properties[4] = properties[4].replace(',', '.')
        if(properties[4] != ''):
            properties[4] = float(properties[4])
        properties[5] = datetime_to_iso(properties[5])
        properties[6] = properties[6].replace(',', '.')
        properties[6] = float(properties[6])
        properties[7] = eval(properties[7])

    data_list.insert(0, ['internal_code', 'barcodes', 'name', 'price', 'promo_price', 'promo_end_at', 'stock', 'visible'])
    #data = [dict(zip(data_list[0], csvRow)) for csvRow in data_list]
    data = []
    for csvRow in data_list:
        item_dict = {
            'internal_code': csvRow[0],
            'barcodes': csvRow[1],
            'name': csvRow[2],
            'price': csvRow[3],
            'promo_price': csvRow[4],
            'promo_end_at': csvRow[5],
            'stock': csvRow[6],
            'visible': csvRow[7],
            'promo_start_at': csvRow[5],
            'unit_type': 'UNI'
        }
        data.append(item_dict)

    data.pop(0)

    #Write data to a Json file
    with open(file_in_same_directory('items.json'), "w") as jsonFile:
        jsonFile.write(json.dumps(data, indent=4, sort_keys=True, default=str))

def main():
    try:
        json_file = csv_to_json()
        response = send_product_to_api(json_file)
        print(f"Reason: {response.reason}\nStatus Code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()