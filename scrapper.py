import requests
from bs4 import BeautifulSoup
import re
import sys
import json


# Scrapper
print("Heureka.cz Price Scrapper v0.6 - (c) 2020 ELS")
print("Usage: python scrapper.py <http[s]://<product>.heureka.cz/product-name-as-found-by-google>")
print()

# saves shell argument into URL var
URL = sys.argv[1]

if "http" in URL or "https" in URL or "-h" in URL:
    pass

else:
    print("Please enter a valid URL (example: https://website.dk/)")
    sys.exit()

if "-h" in URL or "--help" in URL:
    print("This program scraps given Heureka.cz product URL (copy and paste it manually into your terminal from your browser)")
    print("and tries to find the lowest price available and name of the corresponding eshop.\n")
    print("Syntax: python scrapper.py <http[s]://<product>.heureka.cz/product-name-as-found-by-google>")
    print("Example: python scrapper.py https://notebooky.heureka.cz/lenovo-thinkpad-x1-yoga-4-20qf0025mc/#")

    sys.exit()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36"
}

stranka = requests.get(URL, headers=headers)
soup = BeautifulSoup(stranka.content, 'html.parser')

nibble = soup.find(text=re.compile("__advert_product_info = {")) # find specified string
nibble_stripped1 = nibble.strip("var __advert_product_info = ") # cut this string out
nibble_stripped2 = nibble_stripped1.strip(";") # cut ';'

base_dict = json.loads(nibble_stripped2) # convert string to a dict

product_name = base_dict['name']
print("Product name:", product_name)

shops = base_dict['shops']

prices_list = []
for index_number in range(len(shops)):
    name_price_line = shops[str(index_number)]
    prices_list.append(name_price_line['price'])

prices_list_float = []
for price in prices_list:
    prices_list_float.append(float(price))

prices_list_float.sort()
lowest_price = prices_list_float[0]

for index_number in range(len(shops)):
    name_price_line = shops[str(index_number)]
    if name_price_line['price'] == str(lowest_price)+'0':
        shop_name = name_price_line['name']

print("The lowest price:", lowest_price, "CZK")
print("Shop name:", shop_name)
