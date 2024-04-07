import requests

url = "http://localhost:8000/"

# - POST `/mensajes`
ruta_post = url + "mensajes"
nuevo_mensaje ={
        "contenido": "esto se tiene que encriptar"       
    }
post_response = requests.request(method="POST", url=ruta_post, json=nuevo_mensaje)
print(post_response.text)

# - GET `/mensajes`
ruta_get = url + "mensajes"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

# - GET `/mensajes/{id}`
id=1
ruta_get = f"{url}/mensajes/{id}"
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

# - PUT `/mensajes/{id}`
id=1
ruta = f"{url}/mensajes/{id}"
nuevo_mensaje ={
        "contenido": "hola"       
    }
post_response = requests.request(method="PUT", url=ruta, json=nuevo_mensaje)
print(post_response.text)

# - DELETE `/mensajes/{id}`
id=1
ruta_del = f"{url}/mensajes/{id}"
post_response = requests.request(method="DELETE", url=ruta)
print(post_response.text)

