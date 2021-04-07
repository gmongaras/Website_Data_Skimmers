import requests
from bs4 import BeautifulSoup
import csv
import re


def main():
    # Open the webpage
    page = requests.get('https://cs.leandercc.org/Custom2.asp?pagename=members&reason=search&searchtype=name&cid=446&term=%')
    soup = BeautifulSoup(page.content, 'html.parser')

    # Get all the items in the webpage which we will be using.
    items = soup.find_all(lambda tag: tag.name=='table')[2:]

    # Open a file to write the dat to
    csvfile = open('data.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['Company Name', 'Street Address', 'City', 'State', 'Zip Code', 'Phone Number', 'Email'])

    # Get the necissary data from each item.
    for item in items:
        try:
            # Get the only part of the item that's needed
            item = item.find_all(lambda tag: tag.name=='td')[0]

            # Get the two span sections from the item
            span = item.find_all(lambda tag: tag.name=='span')

            #Get the company name
            companyName = check(span[0].find_all(lambda tag: tag.name=='a')[0].text.strip())

            # If the item doesn't have a second span, the item only has
            # a phone number
            try:
                # Get the address. Make sure there is no missing data.
                streetAddress = span[1].find_all(lambda tag: tag.name=='br')[0].next_sibling.strip()
            
                # If the address has an Ste or Bldg number
                if "ste" in str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip()).lower() or "bldg" in str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip()).lower() or "unit" in str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip()).lower() or "#" in str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip()).lower() or "A" in str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip()).lower():
                    # Update the street address
                    streetAddress = str(streetAddress) + " " + str(span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.strip())

                    # Get the city, state, and zipcode
                    csz = span[1].find_all(lambda tag: tag.name=='br')[2].next_sibling.rsplit(" ", 1)

                    # Get the city from csz
                    city = csz[0][:-1].strip()

                    # Get the state and zipCode from csz
                    sz = csz[1].split()

                    # Get the state from sz
                    state = sz[0]

                    # Get the zipCode from sz
                    zipCode = sz[1]

                    # Get the phone number from the item
                    phone = span[1].find_all(lambda tag: tag.name=='br')[3].next_sibling[4:].strip()

                    # Get the email from the item
                    email = item.find_all(lambda tag: tag.name=='a')[1].contents[0]


                # If the address doesn't have an Ste or Bldg number
                else:
                    # Get the city, state, and zipcode
                    csz = span[1].find_all(lambda tag: tag.name=='br')[1].next_sibling.rsplit(" ", 1)

                    # Get the city from csz
                    city = csz[0][:-1].strip()

                    # Get the state and zipCode from csz
                    sz = csz[1].split()

                    # Get the state from sz
                    state = sz[0]

                    # Get the zipCode from sz
                    zipCode = sz[1]

                    # Get the phone number from the item
                    phone = span[1].find_all(lambda tag: tag.name=='br')[2].next_sibling[4:].strip()

                    # Get the email from the item
                    email = item.find_all(lambda tag: tag.name=='a')[1].contents[0]
                

            # If the company only has a phone number
            except:
                continue
            
            #Write the data to the csv file.
            writer.writerow([companyName, streetAddress, city, state, zipCode, phone, email])
        except:
            continue


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
