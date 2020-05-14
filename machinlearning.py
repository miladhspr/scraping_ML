import mysql.connector
from sklearn import tree

#  DB Config
cnx = mysql.connector.connect(
    user="root",
    password='test',
    host='127.0.0.1',
    database='cars'
)
cursor = cnx.cursor()

# DB Query
qry='SELECT * FROM car_details'
cursor.execute(qry)

# Input
x=[]
# Output
y=[]

for car in  cursor:
    car_id , brand, model, date_of_manufacture, distance_traveled, city, price = car
    # change 134,000 to 134000
    # clf need integer
    price = price.replace(',','')
    distance_traveled = distance_traveled.replace(',','')

    x.append([date_of_manufacture, distance_traveled, price])
    y.append([brand, model])

# Make Model
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x,y)

# Insert data you need to findout what's machins think about that
new_data = [[2014, 900000, 1100000000]]
answer = clf.predict(new_data)
print(answer[0])