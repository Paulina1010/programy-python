print('podaj liczbe')
i=int(input())

for x in range(1,i+1):
    lista=[str(x)]
    if(x % 3 == 0):
        lista.append('fizz')
    if(x % 5 == 0):
        lista.append('buzz')
    print(" ".join(lista))
    