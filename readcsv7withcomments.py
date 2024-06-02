#Program dodatkowo wykonuje tylko jedną operację, która jest podana przy wywoływaniu programu np. python readcsv7.py display
from collections import namedtuple
import csv
import sqlite3
import sys

con = sqlite3.connect("database") #połączenie się do bazy database, która zostanie automatycznie utworzona po wywołaniu tego polecenia

if sys.argv[1] == "drop":
    con.execute("DROP TABLE products")
    print("Usunięto tabelę", file=sys.stderr) #stderr oznacza, że komunikat będzie czytelny dla użytkownika
    
elif sys.argv[1] == "create":
    with open('products.csv', newline='') as csvfile: #funkcja open pozwala na odczytanie informarcji z pliku csv
        spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC) #ustawienie nagłówka z pliku csv' QUOTE_NONNUMERIC zamienia słowa bez znaków " " na liczby
        header = next(spamreader) #pobranie nagłówka funkcją next
        con.execute("CREATE TABLE products(%s, %s, %s)" % tuple(header)) #tak nie robić!!! #utworzenie tabeli
    print("Utworzono tabelę", file=sys.stderr)
    
elif sys.argv[1] == "load":
    with open('products.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        header = next(spamreader) #dzięki użyciu next, w pętli for zostanie wzięty pierwszy rekord z tabeli, a nie nagłówek
        products = namedtuple('products', header) #ustawienie nagłówka jako namedtuple, pozwala na powiązanie wartości w kolumnach z nagłówkami
        n = 0
        for emp in map(products._make, spamreader): #pobieranie kolejnych wierszy z pliku 
            con.execute("INSERT INTO products VALUES(?, ?, ?)", emp)
            con.commit() #jest potrzebny commit, ponieważ podczas wywoływania INSERTa w SQLITE automatycznie jest rozpoczynana transakcja, więc musimy ją skomitować
            n += 1 #licznik dodanych rekordów
    print("Załadowano %d rekordy" % n, file=sys.stderr)
    
elif sys.argv[1] == "display":
    try: #obsługa błędu, w którym tabela, której chcemy odczytać dane nie istnieje
        cur = con.execute("SELECT * FROM products")
        empty = True #obsługa błędu, w którym tabela jest pusta
        for row in cur:
            print(*row) #print(row[0], row[1], row[2], ...) * rozwija krotkę albo listę na argumenty
            empty = False
        if empty: #jeśli damych w tabeli nie ma, to warynek jest spełniony i if się wykona. Jeśli dane w tabeli są to wcześniejsza pętla for zamieni emptyna False, więc warunek if nie zostanie spełniony.
            print("Nie ma danych w tabeli", file=sys.stderr)
    except sqlite3.OperationalError: #ten błąd jest w konsoli, gdy tabela nie istnieje
        print("Upps! Tabela nie istnieje", file=sys.stderr)
        sys.exit(1) #zamykamy program z exit code różnym od 0

      
else:
    print("""
Podałeś nieznaną operację. Możesz:
 1) usunąć tabelę - drop
 2) utworzyć tabelę - create
 3) załadować dane do tabeli - load
 4) wyświetlić dane z tabeli - display
            """, file=sys.stderr)
    sys.exit(1)