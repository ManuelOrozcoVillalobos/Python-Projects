import requests
import json
from os.path import exists

json_request_usd = requests.get(f"http://www.floatrates.com/daily/usd.json").json()
with open(f'exchange_usd.json', 'w+', encoding='UTF-8') as json_file_usd:
    json.dump(json_request_usd, json_file_usd)

json_request_eur = requests.get(f"http://www.floatrates.com/daily/eur.json").json()
with open(f'exchange_eur.json', 'w+', encoding='UTF-8') as json_file_eur:
    json.dump(json_request_eur, json_file_eur)

user_currency = input("Please type the currency you want to exchange: ").lower()
exchange_code = input("Please type the currency in which you want to obtain the value: ").lower()

while len(exchange_code) != 0:
    money_amount = input("Please enter the amount of money you have in your original currency: ")
    print('Checking the cache...')
    if exists(f'exchange_{exchange_code}.json') is True:
        print('Oh! it is in the cache!')
        with open(f'exchange_{exchange_code}.json', 'r') as exchange_json:
            exchange_dict = json.load(exchange_json)
        inverse_rate = exchange_dict[user_currency]["inverseRate"]
        print('You received ', round(float(money_amount) * inverse_rate, 2), exchange_code.upper())
        exchange_code = input().lower()

    else:
        print("Sorry, but it is not in the cache!")
        json_request = requests.get(f"http://www.floatrates.com/daily/{exchange_code}.json").json()
        with open(f'exchange_{exchange_code}.json', 'w+', encoding='UTF-8') as json_file:
            json.dump(json_request, json_file)
        with open(f'exchange_{exchange_code}.json', 'r') as exchange_json:
            exchange_dict = json.load(exchange_json)
        inverse_rate = exchange_dict[user_currency]["inverseRate"]
        print('You received ', round(float(money_amount) * inverse_rate, 2), exchange_code.upper())
        exchange_code = input().lower()

