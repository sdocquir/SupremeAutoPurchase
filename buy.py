import time
import sys
import requests
from bs4 import BeautifulSoup
from splinter import Browser

product = "supreme-hanes-tagless-tees"
mainUrl = "http://www.supremenewyork.com/shop/all"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
selectOption = "Large"
namefield = "John Doe"
emailfield = "Test@example.com"
phonefield = "5555555555"
addressfield = "1600 Pennsylvania Avenue NW"
zipfield = "20500"
statefield = "DC"
cctypefield = "master"  # "master" "visa" "american_express"
ccnumfield = "5274576954806318"  # Randomly Generated Data (aka, this isn't mine)
ccmonthfield = "06"  # Randomly Generated Data (aka, this isn't mine)
ccyearfield = "2019"  # Randomly Generated Data (aka, this isn't mine)
cccvcfield = "800"  # Randomly Generated Data (aka, this isn't mine)


def main():
    r = requests.get(mainUrl).text
    if product in r:
        parse(r)


def parse(r):
    soup = BeautifulSoup(r, "html.parser")
    for a in soup.find_all('a', href=True):
        link = a['href']
        checkproduct(link)


def checkproduct(l):
    if product in l:
        prdurl = baseUrl + l
        print(prdurl)
        buyprd(prdurl)


def buyprd(u):
    browser = Browser('firefox')
    url = u
    browser.visit(url)
    # 10|10.5
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added to Cart")
    else:
        print("Error")
        return
    print("checking out")
    browser.visit(checkoutUrl)
    print("Filling Out Billing Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("Filling Out Address")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_state]", statefield)
    print("Filling Out Credit Card Info")

    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[number]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[verification_value]", cccvcfield)
    browser.find_by_css('.terms').click()
    print("Submitting Info")
    browser.find_by_name('commit').click()
    sys.exit(0)


i = 0

while (True):
    main()
    print("On try number " + str(i))
    i = i + 1
    time.sleep(2)
