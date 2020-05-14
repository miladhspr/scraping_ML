import requests
from bs4 import BeautifulSoup
import mysql.connector

brands = list()
models = list()
dms = list()
dts = list()
citys = list()
prices = list()
for i in range(1,21):
    r = requests.get(
        'https://bama.ir/car/all-brands/all-models/all-trims?hasprice=true&page=%d' % i)
    soup = BeautifulSoup(r.text,'html.parser')
    print('insert data from page %d' %i)
    # Brand and Model
    for name in soup.findAll('h2', attrs={'class': 'persianOrder'}):
        name = name.text
        name = name.replace("،", "") if name.find("،") else None
        name = name.replace("(", "") if name.find("(") else None
        name = name.replace(")", "") if name.find(")") else None
        name = name.split()
        brand, model  = name[0],name[1]
        brands.append(brand)
        models.append(model)


    # Date of manufacture
    for date in soup.find_all('span', attrs={'class': 'year-label visible-xs'}):
        date = date.text
        date = date.replace("،", "") if date.find("،") else None
        dms.append(date)


    # Distance traveled
    for dt in soup.find_all('p', attrs={'class': 'price hidden-xs'}):
        dt = dt.text
        dt = dt.replace("کارکرد", "") if dt.find("کارکرد") else None
        dt = dt.replace("صفر", "0") if dt.find("صفر") else None
        dt = dt.strip()
        dts.append(dt)


    # City
    for city in soup.find_all('span', attrs={'class': 'provice-mobile'}):
        city = city.text
        city = city.replace("،", "") if city.find("،") else None
        city = city.strip()
        citys.append(city)

    # Price
    for price in soup.find_all('span', attrs={'itemprop': 'price'}):
        price = price.text
        price = price.strip()
        prices.append(price)

#  Make sure all data set in array
count = 0
for i in range(len(brands)):
    count += 1
print(count)

# DB Config
cnx = mysql.connector.connect(
    user='root' ,password='test',host='127.0.0.1', database='cars'
)
cursor = cnx.cursor()
# INSERT INTO TABLE
for i in range(count):
    qry = ("INSERT INTO car_details (brand, model, date_of_manufacture, distance_traveled, city, price) VALUES ( %s, %s, %s, %s, %s, %s)")
    data_cars = (brands[i], models[i], dms[i], dts[i], citys[i], prices[i])
    cursor.execute(qry, data_cars)
    cnx.commit()

#  Close :)
cursor.close()
cnx.close()

