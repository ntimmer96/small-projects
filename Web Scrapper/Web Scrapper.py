import time
from bs4 import BeautifulSoup
import requests
from twilio.rest import Client

import secrets  # from secrets.py in this folder
def get_page_html(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"}
    page = requests.get(url, headers=headers)
    return page.content


def check_item_in_stock(page_html, store):

    soup = BeautifulSoup(page_html, 'html5lib')
    switch = True
    if (store == "Walmart"):
        if "Out of stock" in str(soup.find("div", {"class" : "prod-ShippingOffer prod-PositionedRelative Grid prod-PriceHero prod-PriceHero-buy-box-update prod-ProductOffer-enhanced"}).get_text):
            switch = False
    elif (store == "Bestbuy"):
        out_of_stock_divs = soup.findAll("button", {"class": "btn btn-disabled btn-lg btn-block add-to-cart-button"})
        switch = (len(out_of_stock_divs) == 0)
    elif (store == "Gamestop"):
        if "Not Available" in str(soup.find("button", {"class" : "add-to-cart btn btn-primary"})["data-gtmdata"]):
            switch = False
    elif (store == "Amazon"):
        print(str(soup.find("div", {"class" : "rightCol rightCol-bbcxoverride"}).get_text))


    return switch

def setup_twilio_client():
    account_sid = secrets.TWILIO_ACCOUNT_SID
    auth_token = secrets.TWILIO_AUTH_TOKEN
    return Client(account_sid, auth_token)

def send_notification(product, trueFalse, store):
    '''twilio_client = setup_twilio_client()
    twilio_client.messages.create(
        body="Your item is available for purchase.",
        from_=secrets.TWILIO_FROM_NUMBER,
        to=secrets.MY_PHONE_NUMBER
    )'''
    if (trueFalse == True):
        print("Item's in stock: " + product + " at " + store)
    else:
        print("Out of stock still: " + product + " at " + store)

def check_inventory(url, store, product):
    page_html = get_page_html(url)
    trueFalse = check_item_in_stock(page_html, store)
    send_notification(product, trueFalse, store)

while True:
    url = ["https://www.walmart.com/ip/PlayStation-5-Console/363472942", "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149",
           "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html", "https://www.amazon.com/PlayStation-5-Console/dp/B08FC5L3RG/ref=sr_1_7?crid=1JKS1AR2IIH68&dchild=1&keywords=playstation+5&qid=1607063103&sprefix=pla%2Caps%2C206&sr=8-7"]
    store = ["Walmart", "Bestbuy", "Gamestop", "Amazon"]
    product = "Playstation 5"
    count = 0

    for i in url:
        check_inventory(i, store[count], product)
        count += 1
    print("------------------\n")
    time.sleep(30)