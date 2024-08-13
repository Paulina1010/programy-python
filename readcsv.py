from collections import namedtuple
import csv
import sqlite3

con = sqlite3.connect(":memory:") #połączenie się do bazy tymczasowej, w RAM
#cur = con.cursor() #utworzenie kursora

with open('products.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    n = next(spamreader)
    products = namedtuple('products', n)
    print(n)
    con.execute("CREATE TABLE products(%s, %s, %s)" % tuple(n)) #tak nie robić!!!
    for emp in map(products._make, spamreader):
        con.execute("INSERT INTO products VALUES(?, ?, ?)", emp)
    for row in con.execute("SELECT * FROM products"):
        print(row)
