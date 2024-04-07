import requests

def consulta(urls,query):    
    # Solicitud POST al servidor GraphQL
    response = requests.post(urls, json={'query': query})
    print(response.text)

# Definir la URL del servidor GraphQL
url = 'http://localhost:8000/graphql'

# Definir las consultas GraphQL simple
query_lista = """
{
        plantas{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
query_add = """
mutation {
    crearPlanta(nombre: "Margarita", especie: "Mar", edad: 12, altura: 10, frutos: true) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
query_search_plantas_por_especie = """
{
    buscarPlantasPorEspecie(especie: "lirio") {
        nombre
        especie
        edad
        altura
        frutos
    }
}
"""
query_search_plantas_por_frutos = """
{
        buscarPlantasPorFrutos{
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
"""
query_update_for_id = """
mutation {
    updatePlanta(id: 1,nombre: "Rosa", especie: "Rositas", edad: 12, altura: 10, frutos: true) {
        planta {
            id
            nombre
            especie
            edad
            altura
            frutos
        }
    }
}
"""
query_delete_for_id = """
mutation {
        deletePlanta(id: 1) {
            planta {
                id
                nombre
                especie
                edad
                altura
                frutos
            }
        }
    }
"""
#  - Crear una planta
consulta(url,query_add)
#  - Listar todas las plantas
consulta(url,query_lista)
#  - Buscar plantas por especie
consulta(url,query_search_plantas_por_especie)
#  - Buscar las plantas que tienen frutos
consulta(url,query_search_plantas_por_frutos)
#  - Actualizar la información de una planta
consulta(url,query_update_for_id)
#  - Eliminar una planta
consulta(url,query_delete_for_id)
