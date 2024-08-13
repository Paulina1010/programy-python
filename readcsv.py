from collections import namedtuple
import csv
import sqlite3
import sys

con = sqlite3.connect("database") #połączenie się do bazy database, która zostanie automatycznie utworzona po wywołaniu tego polecenia
print(sys.argv)

if (sys.argv[1]=="drop"):
    con.execute("DROP TABLE products")
    
else:
    with open('products.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        n = next(spamreader)
        products = namedtuple('products', n)
        print(n)
        if (sys.argv[1]=="create"):
            con.execute("CREATE TABLE products(%s, %s, %s)" % tuple(n)) #tak nie robić!!!
        if (sys.argv[1]=="load"):
            for emp in map(products._make, spamreader):
                con.execute("INSERT INTO products VALUES(?, ?, ?)", emp)
                con.commit()
        if(sys.argv[1]=="display"):
            for row in con.execute("SELECT * FROM products"):
                print(row)
