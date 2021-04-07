import requests
from bs4 import BeautifulSoup
import csv


def main():
    # Open the webpage
    page = requests.get('https://www.cedarparkchamber.org/list/search?q=0-9%2C+a&st=0')
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the items in the webpage which we will be using.
    items = soup.find_all(class_=('mn-list-item-odd'))
    items.append(soup.find_all(class_=('mn-list-item-even')))
    items = items[:-1]

    # Open a file to write the dat to
    csvfile = open('data.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Company Name', 'Street Address', 'City', 'State', 'Zip Code', 'Phone Number'])

    # Get the necissary data from each item.
    for item in items:
        #Get the company name
        companyName = item.find_all(class_='mn-title')[0].text.split("\n")[1].strip()
        
        # Get the address. Make sure there is no missing data.
        streetAddress1 = check(item.find_all(class_='mn-address1'))
        streetAddress2 = " " + check(item.find_all(class_='mn-address2'))
        if streetAddress2 == " N/A":
            streetAddress2 = ""
        streetAddress = streetAddress1 + streetAddress2

        # Get the city
        city = check(item.find_all(class_='mn-cityspan'))

        # Get the state
        state = check(item.find_all(class_="mn-stspan"))

        # Get the zipcode
        zipCode = check(item.find_all(class_="mn-zipspan"))

        # Get the phone number
        phone = check(item.find_all(class_="mn-phone"))
        
        #Write the data to the csv file.
        writer.writerow([companyName, streetAddress, city, state, zipCode, phone])


def check(dataPoint):
    if dataPoint is None or dataPoint == [] or dataPoint == "":
        dataPoint = 'N/A'
    elif isinstance(dataPoint, str):
        return dataPoint
    elif isinstance(dataPoint, list):
        dataPoint = dataPoint[0].text
    else:
        dataPoint = dataPoint.text
    return dataPoint


main()
