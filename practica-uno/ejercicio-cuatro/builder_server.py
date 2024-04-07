from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs
pacientes = {}


class Paciente:
    def __init__(self):
        self.ci = None
        self.nombre = None
        self.apellido = None
        self.genero = None
        self.diagnostico = None
        self.doctor = None 
    
    def __str__(self):
        return f"ci:{self.ci}, nombre:{self.nombre}, apellido:{self.apellido}, genero:{self.genero}, diagnostico:{self.diagnostico}, doctor:{self.doctor} "

class PacienteBuilder:
    def __init__(self):
        self.paciente = Paciente()    

    def set_ci(self, ci):
        self.paciente.ci = ci
        
    def set_nombre(self,nombre):
        self.paciente.nombre = nombre
        
    def set_apellido(self,apellido):
        self.paciente.apellido = apellido
    
    def set_genero(self,genero):
        self.paciente.genero = genero
        
    def set_diagnostico(self, diagnostico):
        self.paciente.diagnostico = diagnostico
    
    def set_doctor(self, doctor):
        self.paciente.doctor = doctor
    
    def get_paciente(self):
        return self.paciente
    
class Hospital:
    def __init__(self,builder):
        self.builder = builder

        
    def create_paciente(self,ci,nombre,apellido,genero,diagnostico,doctor):       
        self.builder.set_ci(ci)
        self.builder.set_nombre(nombre)
        self.builder.set_apellido(apellido)
        self.builder.set_genero(genero)
        self.builder.set_diagnostico(diagnostico)
        self.builder.set_doctor(doctor)
        
        return self.builder.get_paciente()
        
class HostpitalService:
    def __init__(self):
        self.builder = PacienteBuilder()
        self.hospital = Hospital(self.builder)
        
    def create_paciente(self, post_data):       
        ci = post_data.get('ci', None)
        nombre = post_data.get('nombre', None)
        apellido = post_data.get('apellido', None)
        genero = post_data.get('genero', None)
        diagnostico = post_data.get('diagnostico', None)
        doctor = post_data.get('doctor', None)
        
        paciente = self.hospital.create_paciente(ci, nombre,apellido,genero,diagnostico,doctor)
        pacientes[len(pacientes)+1]=paciente
        
        return paciente
    
    def read_pacientes(self):
        return {index: paciente.__dict__ for index, paciente in pacientes.items()}
    
    def update_paciente(self, ci, data):
        for index, paciente in pacientes.items():
            if paciente.ci == ci:               
                nombre = data.get("nombre", None)
                apellido = data.get("apellido", None)
                genero = data.get("genero", None)
                diagnostico = data.get("diagnostico", None)
                doctor = data.get("doctor", None)
                
                if nombre is not None:
                    paciente.nombre = nombre
                if apellido is not None:
                    paciente.apellido = apellido
                if genero is not None:
                    paciente.genero = genero
                if diagnostico is not None:
                    paciente.diagnostico = diagnostico
                if doctor is not None:
                    paciente.doctor = doctor

                return paciente

        return None

        
    def delete_paciente(self, ci):
        for index, paciente in pacientes.items():
            if paciente.ci == ci:
                del pacientes[index]
                return paciente

        return None
    
    def buscar_paciente_por_doctor(self, doctor):
        pacientes_encontrados = []
        for paciente in pacientes.values():
            if paciente.doctor == doctor:
                pacientes_encontrados.append(paciente)
        return pacientes_encontrados

    def buscar_paciente_por_diagnostico(self, diagnostico):
        pacientes_encontrados = []
        for paciente in pacientes.values():
            if paciente.diagnostico == diagnostico:
                pacientes_encontrados.append(paciente)
        return pacientes_encontrados


class HTTPDataHandler:
    @staticmethod
    def handle_response(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers['Content-Length'])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))


class PacienteHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.controller = HostpitalService()
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/pacientes":
            if "doctor" in query_params:
                doctor = query_params["doctor"][0]
                pacientes_por_doctor = self.controller.buscar_paciente_por_doctor(doctor)
                response_data = {index: paciente.__dict__ for index, paciente in enumerate(pacientes_por_doctor, start=1)}
                HTTPDataHandler.handle_response(self, 200, response_data)
            elif "diagnostico" in query_params:
                diagnostico = query_params["diagnostico"][0]
                pacientes_por_diagnostico = self.controller.buscar_paciente_por_diagnostico(diagnostico)
                response_data = {index: paciente.__dict__ for index, paciente in enumerate(pacientes_por_diagnostico, start=1)}
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                response_data = self.controller.read_pacientes()
                HTTPDataHandler.handle_response(self, 200, response_data)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_POST(self):
        if self.path == '/pacientes':
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.create_paciente(data)            
            HTTPDataHandler.handle_response(self, 201, response_data.__dict__)
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_PUT(self):
        if self.path.startswith("/pacientes/"):
            index = int(self.path.split("/")[2])
            data = HTTPDataHandler.handle_reader(self)
            response_data = self.controller.update_paciente(index, data)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})

    def do_DELETE(self):
        if self.path.startswith("/pacientes/"):
            ci = int(self.path.split("/")[2])
            deleted_paciente = self.controller.delete_paciente(ci)
            if deleted_paciente:
                HTTPDataHandler.handle_response(
                    self, 200, {"message": "paciente eliminada correctamente"}
                )
            else:
                HTTPDataHandler.handle_response(
                    self, 404, {"Error": "Índice de paciente no válido"}
                )
        else:
            HTTPDataHandler.handle_response(self, 404, {"Error": "Ruta no existente"})


def run(server_class=HTTPServer, handler_class=PacienteHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
