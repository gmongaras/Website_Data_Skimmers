import requests
from bs4 import BeautifulSoup
import csv


def main():
    # Open the webpage
    page = requests.get('https://members.libertyhillchamber.org/list/search?q=0-9%2c+a&o=alpha')
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the items in the webpage which we will be using.
    items = soup.find_all(class_=('col-md-4'))

    # Open a file to write the dat to
    csvfile = open('data.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Company Name', 'Street Address', 'City', 'State', 'Zip Code', 'Phone Number'])

    # Get the necissary data from each item.
    for item in items:
        #Get the company name
        try:
            companyName = item.find_all(class_='gz-img-placeholder')[0].text
        except:
            companyName = item.find_all(class_='gz-card-title')[0].text.strip('\n')

        #Get the address and phone number. Make sure there is no missing data.
        streetAddress = item.find_all(class_='gz-street-address')
        streetAddress = check(streetAddress)
        city = item.find_all(class_='gz-address-city')#[0].text
        city = check(city)
        state = item.find('span', itemprop='addressRegion')
        state = check(state)
        zipCode = item.find('span', itemprop='postalCode')
        zipCode = check(zipCode)
        phone = item.find('span', itemprop='telephone')
        phone = check(phone)

        # Since there is a pice of data that is missing from the website, I will
        #write it in manually.
        if companyName == "Schlotzsky's":
            writer.writerow(['Simplified Engineering', '407 Forest Street', 'Liberty Hill', 'TX', '78642', '(512) 947-4141'])

        #Write the data to the csv file.
        writer.writerow([companyName, streetAddress, city, state, zipCode, phone])


def check(dataPoint):
    if dataPoint is None or dataPoint == []:
        dataPoint = 'N/A'
    elif isinstance(dataPoint, list):
        dataPoint = dataPoint[0].text
    else:
        dataPoint = dataPoint.text
    return dataPoint


main()
