import requests
from bs4 import BeautifulSoup
import csv


def main():
    # Open the webpage
    page = requests.get('https://business.georgetownchamber.org/list/search?q=0-9%2c+a&o=alpha')
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

        # If the company is RPI Inc., hard code it
        if companyName == "RPI, Inc":
            writer.writerow(["RPI Inc.", "1880 S Dairy Ashford Rd", "Houston", "TX", "77077", "(128) 155-84444"])
            continue
        
        #Get the address and phone number. Make sure there is no missing data.
        streetAddress = item.find_all(class_='gz-street-address')
        streetAddress = check(streetAddress).strip('"')
        city = item.find_all(class_='gz-address-city')
        city = check(city)
        
        try:
            czp = item.find(itemprop="citystatezip").text.split("\n")
            for i in range(0, len(czp)):
                if czp[i] != '':
                    if ord(czp[i][-1]) == 32:
                        czp[i] = czp[i][:-1]
            if czp[2].upper() == "TEXAS" or czp[2].upper() == "TX" or czp[2] == "US":
                state = czp[2]
                zipCode = czp[3]
            else:
                state = czp[1]
                zipCode = czp[2]
            if item.find_all(class_='gz-fal gz-fa-phone') != []:
                phone = item.find_all(class_=None)[-1]
            else:
                phone = "N/A"
        except:
            if item.find_all(class_='gz-fal gz-fa-phone') != []:
                if item.find_all(class_="gz-street-address") != []:
                    state = item.find_all(class_=None)[-3]
                    zipCode = item.find_all(class_=None)[-2]
                    phone = item.find_all(class_=None)[-1]
                else:
                    state = ""
                    zipCode = ""
                    phone = item.find_all(class_=None)[-1]
            else:
                state = item.find_all(class_=None)[-2]
                zipCode = item.find_all(class_=None)[-1]
                phone = "N/A"
        state = check(state)
        zipCode = check(zipCode)
        phone = check(phone)
        
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
