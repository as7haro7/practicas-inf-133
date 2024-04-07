from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
# Base de datos simulada de animales
animales = {}

class AnimaZoologico:
    def __init__(self, nombre, especie, genero, edad, peso):
        self.nombre=nombre
        self.especie=especie
        self.genero=genero
        self.edad=edad
        self.peso=peso

class Mamifero(AnimaZoologico):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__(nombre, "mamifero", genero, edad, peso)

class Ave(AnimaZoologico):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__(nombre, "ave", genero, edad, peso)
        
class Reptil(AnimaZoologico):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__(nombre, "reptil", genero, edad, peso)
        
class Anfibio(AnimaZoologico):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__(nombre, "anfibio", genero, edad, peso)

class Pez(AnimaZoologico):
    def __init__(self, nombre, genero, edad, peso):
        super().__init__(nombre, "pez", genero, edad, peso)
       
class ZoologicoFactory:
    @staticmethod
    def create_animal(nombre, especie, genero, edad, peso):
        if especie == "mamifero":
            return Mamifero(nombre, genero, edad, peso)
        elif especie == "ave":
            return Ave(nombre, genero, edad, peso)
        elif especie == "reptil":
            return Reptil(nombre, genero, edad, peso)
        elif especie == "anfibio":
            return Anfibio(nombre, genero, edad, peso)
        elif especie == "pez":
            return Pez(nombre, genero, edad, peso)
        else:
            raise ValueError("Especie de animal no válida")
        
class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

# clase para manejar los metodos de el zoologico
class ZoologicoService:
    def __init__(self):
        self.factory = ZoologicoFactory()
    
    def add_animal(self, data):
        nombre = data.get("nombre", None)
        especie = data.get("especie", None)
        genero = data.get("genero", None)
        edad = data.get("edad", None)
        peso = data.get("peso", None)

        animal_zoologico = self.factory.create_animal(
            nombre,especie,genero,edad,peso
        )
        animales[len(animales) + 1] = animal_zoologico
        return animal_zoologico
    
    def list_animales(self):
        return {index: animal.__dict__ for index, animal in animales.items()}
    
    def update_animal(self, animal_id, data):
        if animal_id in animales:
            animal = animales[animal_id]
            nombre = data.get("nombre", None)
            especie = data.get("especie", None)
            genero = data.get("genero", None)
            edad = data.get("edad", None)
            peso = data.get("peso", None)
            if nombre:
                animal.nombre = nombre
            if especie:
                animal.especie = especie
            if genero:
                animal.genero = genero
            if edad:
                animal.edad = edad
            if peso:
                animal.peso = peso
            return animal
        else:
            raise None
        
    def delete_animal(self, animal_id):
        if animal_id in animales:
            del animales[animal_id]
            return {"message": "animal eliminado"}
        else:
            return None
        
    def search_animal_for_especie(self,especie):
        animales_encontrados = []
        for animal in animales.values():
            if animal.especie == especie:
                animales_encontrados.append(animal)
        return animales_encontrados

    def search_animal_for_genero(self, genero):
        animales_encontrados = []
        for animal in animales.values():
            if animal.genero == genero:
                animales_encontrados.append(animal)
        return animales_encontrados


# clase para manegar las petiticiones post,get,put,delelete
class ZoologicoRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.zoologico_service = ZoologicoService()
        super().__init__(*args, **kwargs)
    
    def do_POST(self):
        if self.path == "/animales":
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.add_animal(data)
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            if "especie" in query_params:
                especie = query_params["especie"][0]
                animales_filtrados = self.zoologico_service.search_animal_for_especie(especie)
                if animales_filtrados:
                    animales_serializables = [animal.__dict__ for animal in animales_filtrados]
                    HTTPDataHandler.handle_response(self, 200, animales_serializables)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "No se encontraron animales de esa especie"})
            elif "genero" in query_params:
                genero = query_params["genero"][0]
                animales_filtrados = self.zoologico_service.search_animal_for_genero(genero)
                if animales_filtrados:
                    animales_serializables = [animal.__dict__ for animal in animales_filtrados]
                    HTTPDataHandler.handle_response(self, 200, animales_serializables)
                else:
                    HTTPDataHandler.handle_response(self, 404, {"message": "No se encontraron animales de ese género"})
            else:
                response_data = self.zoologico_service.list_animales()
                animales_serializables = {index: animal.__dict__ for index, animal in response_data.items()}
                HTTPDataHandler.handle_response(self, 200, animales_serializables)
        else:
            HTTPDataHandler.handle_response(self, 404, {"message": "Ruta no encontrada"})

                
    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.zoologico_service.update_animal(animal_id, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            response_data = self.zoologico_service.delete_animal(animal_id)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"message": "Animal no encontrado"}
                )
        else:
            HTTPDataHandler.handle_response(
                self, 404, {"message": "Ruta no encontrada"}
            )

    

# classe para manejar el servidor http
def main():
    try:
        server_address = ("", 8000)
        httpd = HTTPServer(server_address, ZoologicoRequestHandler)
        print("Iniciando servidor HTTP en puerto 8000...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor HTTP")
        httpd.socket.close()


if __name__ == "__main__":
    main()
