import requests

url = "http://localhost:8000/"


ruta_get = url + "pacientes"


#  - Crear un paciente
nuevo_paciente = {   
    "ci": 798354,
    "nombre": "Xiomara",
    "apellido": "Machaca",
    "genero": "F",
    "diagnostico": "Depresión",
    "doctor": "Pedro Pérez"
}
post_response = requests.request(method="POST", url=ruta_get, json=nuevo_paciente)
print(post_response.text)

#  - Listar todos los pacientes
get_response = requests.request(method="GET", url=ruta_get)
print(get_response.text)

#  - Buscar pacientes por CI
ci=1233333
ruta=ruta_get+"/"+str(ci)
get_response = requests.request(method="GET", url=ruta)
print(get_response.text)

#  - Listar a los pacientes que tienen diagnostico de Diabetes
diagnostico="Diabetes"
ruta=f"{ruta_get}?diagnostico={diagnostico}"
get_response = requests.request(method="GET", url=ruta)
print(get_response.text)

#  - Listar a los pacientes que atiende el Doctor Pedro Pérez
doctor="Pedro Pérez"
ruta=f"{ruta_get}?doctor={doctor}"
get_response = requests.request(method="GET", url=ruta)
print(get_response.text)

#  - Actualizar la información de un paciente
ci=798354
ruta=ruta_get+"/"+str(ci)
datos_paciente = {   
    "ci": 798354,
    "nombre": "Xiomara",
    "apellido": "Arias",
    "genero": "F",
    "diagnostico": "Depresión",
    "doctor": "Pedro Pérez"
}
post_response = requests.request(method="PUT", url=ruta, json=datos_paciente)
print(post_response.text)

#  - Eliminar un paciente
ci=1233333
ruta=ruta_get+"/"+str(ci)
post_response = requests.request(method="DELETE", url=ruta)
print(post_response.text)
