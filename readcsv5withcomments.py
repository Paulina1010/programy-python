from collections import namedtuple
import csv
import sqlite3

con = sqlite3.connect(":memory:") #połączenie się do bazy tymczasowej, w RAM
#cur = con.cursor() #utworzenie kursora, obiekt, który pozwala
#execute musi być robone kursorem

with open('products.csv', newline='') as csvfile: #wczytywanie linii z pliku csv
    spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC) #wczytywanie poszczególnych wartości z pliku csv, wartości bez cudzyłowów są zamieniane na liczby
    n = next(spamreader)
    products = namedtuple('products', n) #utworzenie namedtuple, aby wartości były powiązane z kolumną, z której pochodzą
    print(n)
    con.execute("CREATE TABLE products(%s, %s, %s)" % tuple(n)) #tak nie robić!!! #utworzenie tabeli w bazie sqlite; tabela(nazwy kolumny)
    for emp in map(products._make, spamreader): #wczytywanie poszczególnych linii używając namedtuple; z tego powodu używamy funkcji __make
        con.execute("INSERT INTO products VALUES(?, ?, ?)", emp) #zapisanie wyników do tabeli sql
    for row in con.execute("SELECT * FROM products"): #odczytanie wartości z tabeli w sql
        print(row)
