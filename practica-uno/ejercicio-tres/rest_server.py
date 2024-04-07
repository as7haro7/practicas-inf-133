from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

pacientes = [
    {
        "id": 1,
        "ci": 1233333,
        "nombre": "Pedrito",
        "apellido": "García",
        "genero": "M",
        "diagnostico": "Sida",
        "doctor": "Alan Brito"
    },
    {
        "id": 2,
        "ci": 4567777,
        "nombre": "María",
        "apellido": "Martínez",
        "genero": "F",
        "diagnostico": "Hipertensión",
        "doctor": "Elena López"
    },
    {
        "id": 3,
        "ci": 7899999,
        "nombre": "Juan",
        "apellido": "Pérez",
        "genero": "M",
        "diagnostico": "Diabetes",
        "doctor": "Carlos Ruiz"
    },
     {
        "id": 4,
        "ci": 1122334,
        "nombre": "Ana",
        "apellido": "López",
        "genero": "F",
        "diagnostico": "Asma",
        "doctor": "María Rodríguez"
    },
    {
        "id": 5,
        "ci": 4455667,
        "nombre": "Carlos",
        "apellido": "González",
        "genero": "M",
        "diagnostico": "Gripe",
        "doctor": "José Martínez"
    },
    {
        "id": 6,
        "ci": 7788990,
        "nombre": "Sofía",
        "apellido": "Diabetes",
        "genero": "F",
        "diagnostico": "Artritis",
        "doctor": "Ana Pérez"
    },
    {
        "id": 7,
        "ci": 1020304,
        "nombre": "Manuel",
        "apellido": "Fernández",
        "genero": "M",
        "diagnostico": "Cáncer",
        "doctor": "Pedro Pérez"
    },
    {
        "id": 8,
        "ci": 4050607,
        "nombre": "Laura",
        "apellido": "Hernández",
        "genero": "F",
        "diagnostico": "Depresión",
        "doctor": "Pedro Pérez"
    }
]

class PacientesService:
    @staticmethod
    def find_paciente(ci):
        return next(
            (paciente for paciente in pacientes if paciente["ci"] == ci),
            None,
        )

    @staticmethod
    def filter_pacientes_by_diagnostico(diagnostico):
        return [
            paciente for paciente in pacientes if paciente["diagnostico"] == diagnostico
        ]
    @staticmethod
    def filter_pacientes_by_doctor(doctor):
        return [
            paciente for paciente in pacientes if paciente["doctor"] == doctor
        ]

    @staticmethod
    def add_paciente(data):
        data["id"] = len(pacientes) + 1
        pacientes.append(data)
        return pacientes

    @staticmethod
    def update_paciente(ci, data):
        pacientes = PacientesService.find_paciente(ci)
        if pacientes:
            pacientes.update(data)
            return pacientes
        else:
            return None

    @staticmethod
    def delete_paciente(ci):
        for paciente in pacientes:
            if(paciente["ci"]==ci):
                pacientes.remove(paciente)
        return pacientes


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


        if parsed_path.path == "/pacientes":
            if "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_diagnostico(
                    diagnostico
                )
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            
            elif "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_filtrados = PacientesService.filter_pacientes_by_doctor(
                    doctor
                )
                if pacientes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, pacientes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
        elif self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            paciente = PacientesService.find_paciente(ci)
            if paciente:
                HTTPResponseHandler.handle_response(self, 200, [paciente])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/pacientes":
            data = self.read_data()
            pacientes = PacientesService.add_paciente(data)
            HTTPResponseHandler.handle_response(self, 201, pacientes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            data = self.read_data()
            pacientes = PacientesService.update_paciente(ci, data)
            if pacientes:
                HTTPResponseHandler.handle_response(self, 200, pacientes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Paciente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[-1])
            pacientes = PacientesService.delete_paciente(ci)
            HTTPResponseHandler.handle_response(self, 200, pacientes)
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
