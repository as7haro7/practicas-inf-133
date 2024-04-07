from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs

mensajes = []


class Mensaje:
    def __init__(self, id, contenido, encriptado):
        self.id = id
        self.contenido = contenido
        self.encriptado = encriptado


class MensajeService:
    @staticmethod
    def find_mensaje(id):
        return next(
            (mensaje for mensaje in mensajes if mensaje.id == id), None
        )
    
    @staticmethod
    def encriptar(texto, desplazamiento=3):
        alfabeto = "abcdefghijklmnñopqrstuvwxyzáéíóúüABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚÜ"
        resultado = ""
        for letra in texto:
            if letra in alfabeto:
                indice = alfabeto.index(letra)
                nuevo_indice = (indice + desplazamiento) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += letra
        return resultado

    @staticmethod
    def add_mensaje(data):
        id = len(mensajes) + 1
        mensaje = Mensaje(id, data["contenido"], MensajeService.encriptar(data["contenido"]))
        mensajes.append(mensaje)
        return mensaje

    @staticmethod
    def update_mensaje(id, data):
        mensaje = next((m for m in mensajes if m.id == id), None)
        if mensaje:
            mensaje.contenido = data.get("contenido", mensaje.contenido)
            mensaje.encriptado = MensajeService.encriptar(mensaje.contenido)
            return mensaje
        else:
            return None

    @staticmethod
    def delete_mensaje(id):
        mensaje = next((m for m in mensajes if m.id == id), None)
        if mensaje:
            mensajes.remove(mensaje)
            return True
        else:
            return False


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

        if parsed_path.path == "/mensajes":
            HTTPResponseHandler.handle_response(
                self, 200, [mensaje.__dict__ for mensaje in mensajes]
            )
        elif self.path.startswith("/mensajes/"):
            id = int(self.path.split("/")[-1])
            mensaje = MensajeService.find_mensaje(id)
            if mensaje:
                HTTPResponseHandler.handle_response(self, 200, [mensaje.__dict__])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/mensajes":
            data = self.read_data()
            mensaje = MensajeService.add_mensaje(data)
            HTTPResponseHandler.handle_response(self, 201, mensaje.__dict__)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        id = int(parsed_path.path.split("/")[-1])
        data = self.read_data()
        mensaje = MensajeService.update_mensaje(id, data)
        if mensaje:
            HTTPResponseHandler.handle_response(self, 200, mensaje.__dict__)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Mensaje no encontrado"}
            )

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        id = int(parsed_path.path.split("/")[-1])
        success = MensajeService.delete_mensaje(id)
        if success:
            HTTPResponseHandler.handle_response(self, 200, {"message": "Mensaje eliminado"})
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Mensaje no encontrado"}
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
