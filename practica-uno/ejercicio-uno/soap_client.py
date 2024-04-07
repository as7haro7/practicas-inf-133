from zeep import Client

client = Client('http://localhost:8000')

a=2
b=3

result = client.service.Sumar(a,b)
print(f'{a} + {b} = {result}')

result = client.service.Restar(a,b)
print(f'{a} - {b} = {result}')

result = client.service.Multiplicar(a,b)
print(f'{a} * {b} = {result}')


result = client.service.Dividir(a,b)
print(f'{a} / {b} = {result}')



