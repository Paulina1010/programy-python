from collections import namedtuple
import csv

with open('products.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    products = namedtuple('products', next(spamreader))

    for emp in map(products._make, spamreader):
        print(emp)