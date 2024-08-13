#Program dodatkowo wykonuje tylko jedną operację, która jest podana przy wywoływaniu programu np. python readcsv7.py display
from collections import namedtuple
import csv
import sqlite3
import sys

con = sqlite3.connect("database") #połączenie się do bazy database, która zostanie automatycznie utworzona po wywołaniu tego polecenia

if sys.argv[1] == "drop":
    con.execute("DROP TABLE products")
    print("Usunięto tabelę", file=sys.stderr)
    
elif sys.argv[1] == "create":
    with open('products.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        header = next(spamreader)
        con.execute("CREATE TABLE products(%s, %s, %s)" % tuple(header)) #tak nie robić!!!
    print("Utworzono tabelę", file=sys.stderr)
    
elif sys.argv[1] == "load":
    with open('products.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        header = next(spamreader)
        products = namedtuple('products', header)
        n = 0
        for emp in map(products._make, spamreader):
            con.execute("INSERT INTO products VALUES(?, ?, ?)", emp)
            con.commit() #jest potrzebny commit, ponieważ podczas wywoływania INSERTa w SQLITE automatycznie jest rozpoczynana transakcja, więc musimy ją skomitować
            n += 1 #licznik dodanych rekordów
    print("Załadowano %d rekordy" % n, file=sys.stderr)
    
elif sys.argv[1] == "display":
    try:
        cur = con.execute("SELECT * FROM products")
        empty = True
        for row in cur:
            print(*row) #print(row[0], row[1], row[2], ...) * rozwija krotkę albo listę na argumenty
            empty = False
        if empty:
            print("Nie ma danych w tabeli", file=sys.stderr)
    except sqlite3.OperationalError:
        print("Upps! Tabela nie istnieje", file=sys.stderr)
        sys.exit(1)

      
else:
    print("""
Podałeś nieznaną operację. Możesz:
 1) usunąć tabelę - drop
 2) utworzyć tabelę - create
 3) załadować dane do tabeli - load
 4) wyświetlić dane z tabeli - display
            """, file=sys.stderr)
    sys.exit(1)