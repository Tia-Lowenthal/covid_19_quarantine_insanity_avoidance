# The following program tracks the price of specific items I like once a day and notifies me if their price decreases

from bs4 import BeautifulSoup
import requests
import json
import time
from pushsafer import init, Client

NUM_SECS_A_DAY = 86400

# dict of URLs of items of interest
itemUrls = {
    "cord-jacket": "https://www.princesshighway.com.au/charlie-girl-jacket-34865.html",
    "wrap-knit": "https://www.princesshighway.com.au/ballet-wrap-knit.html",
    "puff-dress": "https://www.princesshighway.com.au/sadie-dress.html",
    "dream-dress": "https://www.princesshighway.com.au/honey-cord-pinny.html"
}

# dict of item prices
currPriceDict = {
    "cord-jacket": 70.4,
    "wrap-knit": 62.4,
    "puff-dress": 70.4,
    "dream-dress": 70.4
}

# gets the price from the html
def get_price(content):
    div = content.find('div', attrs={"class": "col-md-6 col-lg-6 col-sm-6 col-xs-6 special-price text-left text-center-xs"})
    price = div.find('span',  attrs={"class": "price"})
    prettyPrice = price.getText().strip()[1:]
    price = float(prettyPrice)
    return price

# gets the html from a webpage
def check_price(url):
    response = requests.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    return get_price(content)
    
# sends email notifying of item price decrease - INCOMPLETE
def send_alert(item, price):
    message = item + " has dropped to $" + str(price) + "!"
    init("<private-key>")
    Client("").send_message(message, "Price Drop!", "<device-ID>", "1", "4", "2", "https://www.pushsafer.com", "Open Pushsafer", "0", "0", "ex", "0", "0", "data:image/gif;base64,R0L...Bow==", "data:image/jpeg;base64,C4s...Cc1==", "data:image/png;base64,G0G...H5R==")


# iterates through items and updates their prices
# if the price of an item has decreased, it sends an alert
def check_items_prices():
    for item in itemUrls.keys():
        url = itemUrls[item]
        newPrice = check_price(url)
        # check for price drops greater than $1
        if currPriceDict[item] - newPrice > 1.0:
            send_alert(item, newPrice)
            currPriceDict[item] = newPrice

# perform price checks once a day
while True:
    check_items_prices()
    time.sleep(NUM_SECS_A_DAY)
