from collections import namedtuple
import csv

products = namedtuple('products', 'Product, Value, Price')

for emp in map(products._make, csv.reader(open("products.csv", newline=''), delimiter=';', quoting=csv.QUOTE_NONNUMERIC)):
    print(emp)
    #print(emp.Product, emp.Value, emp.Price)
    
 