import csv

with open('products.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
    for row in spamreader:
        for i in row:
            print(i, type(i).__name__, end=' | ')
        print()