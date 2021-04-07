import requests
from bs4 import BeautifulSoup
import csv
import re
import time


def main():
    # Open the webpage
    page = requests.get('https://web.roundrockchamber.org/directory/results.aspx?Keywords=%&AdKeyword=%&SearchCategories=False&SearchNames=False&SearchOnlyMembers=False')
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the items in the webpage which we will be using.
    items = soup.find_all(class_=('ListingResults_All_CONTAINER'))
    
    # Open a file to write the dat to
    csvfile = open('data.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Company Name', 'Street Address', 'City', 'State', 'Zip Code', 'Phone Number'])

    # Get the necissary data from each item.
    for item in items:
        # Get the item level to correctly get each tag
        level = re.findall(r'\d+', str(item.find_all(lambda tag: tag.name=='div')[0]))[0]
        
        #Get the company name
        companyName = item.find_all(class_='ListingResults_Level'+level+'_HEADER')[0].find_all(lambda tag: tag.name=='a')[1].text
        
        # Get the address. Make sure there is no missing data.
        streetAddress = item.find_all(itemprop="street-address")[0].text
    
        # Get the city
        city = item.find_all(itemprop="locality")[0].text

        # Get the state
        state = item.find_all(itemprop="region")[0].text

        # Get the zipcode
        zipCode = item.find_all(itemprop="postal-code")[0].text

        # Get the phone number
        try:
            phone = check(item.find_all(class_="ListingResults_Level"+level+"_PHONE1")[0].text)
        except:
            phone = "N\A"
        
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
