import requests

url = "http://localhost:8000/"
ruta_gen = url + "animales"


# - Crear un animal
nuevo_animal = {
    "nombre": "Perro",
    "especie": "pardus",
    "genero": "Michitus",
    "edad": 12,
    "peso": 80
}
post_response = requests.request(method="POST", url=ruta_gen, json=nuevo_animal)
print(post_response.text)

# - Listar todos los animales
get_response = requests.request(method="GET", url=ruta_gen)
print(get_response.text)

# - Buscar animales por especie
especie="pardus"
ruta=f"{ruta_gen}?especie={especie}"
get_response = requests.request(method="GET", url=ruta)
print(get_response.text)

# - Buscar animales por género
genero="Hembra"
ruta=f"{ruta_gen}?genero={genero}"
get_response = requests.request(method="GET", url=ruta)
print(get_response.text)

# - Actualizar la información de un animal
id=1
ruta=ruta_gen+"/"+str(id)
datos_animal = {
    "nombre": "Tigre",
    "especie": "Panthera tigris",
    "genero": "Hembra",
    "edad": 7,
    "peso": 200
}
post_response = requests.request(method="PUT", url=ruta, json=datos_animal)
print(post_response.text)

# - Eliminar un animal
id=1
ruta=ruta_gen+"/"+str(id)
post_response = requests.request(method="DELETE", url=ruta)
print(post_response.text)
