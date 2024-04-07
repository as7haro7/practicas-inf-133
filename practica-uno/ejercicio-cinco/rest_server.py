from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

animales = [
    {
        "id": 1,
        "nombre": "Condor",
        "especie": "Vultur gryphus",
        "genero": "Macho",
        "edad": 15,
        "peso": 10
    },
    {
        "id": 2,
        "nombre": "Leon",
        "especie": "Panthera leo",
        "genero": "Hembra",
        "edad": 8,
        "peso": 150
    },
    {
        "id": 3,
        "nombre": "Tigre",
        "especie": "Panthera tigris",
        "genero": "Macho",
        "edad": 6,
        "peso": 200
    },
    {
        "id": 4,
        "nombre": "Elefante",
        "especie": "Loxodonta africana",
        "genero": "Hembra",
        "edad": 25,
        "peso": 5000
    },
    {
        "id": 5,
        "nombre": "Oso",
        "especie": "Ursidae",
        "genero": "Macho",
        "edad": 10,
        "peso": 300
    },
    {
        "id": 6,
        "nombre": "Jirafa",
        "especie": "Giraffa camelopardalis",
        "genero": "Hembra",
        "edad": 12,
        "peso": 800
    },
    {
        "id": 7,
        "nombre": "Hipopotamo",
        "especie": "Hippopotamus amphibius",
        "genero": "Macho",
        "edad": 20,
        "peso": 2000
    },
    {
        "id": 8,
        "nombre": "Cebra",
        "especie": "Equus quagga",
        "genero": "Hembra",
        "edad": 7,
        "peso": 250
    },
    {
        "id": 9,
        "nombre": "Rinoceronte",
        "especie": "Rhinocerotidae",
        "genero": "Macho",
        "edad": 15,
        "peso": 2000
    },
    {
        "id": 10,
        "nombre": "Leopardo",
        "especie": "Panthera pardus",
        "genero": "Hembra",
        "edad": 9,
        "peso": 100
    }
]

class AnimalesService:
    @staticmethod
    def find_animal(id):
        return next(
            (animal for animal in animales if animal["id"] == id),
            None,
        )
        
    @staticmethod
    def filter_by_especie(especie):
        return [animal for animal in animales if animal["especie"] == especie]

    @staticmethod
    def filter_by_genero(genero):
        return [animal for animal in animales if animal["genero"] == genero]

    @staticmethod
    def add_animal(data):
        data["id"] = len(animales) + 1
        animales.append(data)
        return animales

    @staticmethod
    def update_animal(id, data):
        animal = AnimalesService.find_animal(id)
        if animal:
            animal.update(data)
            return animal
        else:
            return None

    @staticmethod
    def delete_animal(id):
        for animal in animales:
            if animal["id"] == id:
                animales.remove(animal)
                break
        return animales


class HTTPResponseHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/animales":
            especie = query_params.get("especie", [None])[0]
            genero = query_params.get("genero", [None])[0]

            if especie:
                animales_filtrados = AnimalesService.filter_by_especie(especie)
            elif genero:
                animales_filtrados = AnimalesService.filter_by_genero(genero)
            else:
                animales_filtrados = animales

            if animales_filtrados:
                HTTPResponseHandler.handle_response(self, 200, animales_filtrados)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "No se encontraron animales que coincidan con los criterios de búsqueda"})
        elif parsed_path.path.startswith("/animales/"):
            animal_id = int(parsed_path.path.split("/")[-1])
            animal = AnimalesService.find_animal(animal_id)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(self, 404, {"Error": "Animal no encontrado"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/animales":
            data = self.read_data()
            animal = AnimalesService.add_animal(data)
            HTTPResponseHandler.handle_response(self, 201, animal)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            data = self.read_data()
            animal = AnimalesService.update_animal(animal_id, data)
            if animal:
                HTTPResponseHandler.handle_response(self, 200, animal)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Animal no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/animales/"):
            animal_id = int(self.path.split("/")[-1])
            animal = AnimalesService.delete_animal(animal_id)
            HTTPResponseHandler.handle_response(self, 200, animal)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
