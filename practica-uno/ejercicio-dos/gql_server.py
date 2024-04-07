from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from graphene import ObjectType, String, Int, List,Boolean, Schema, Field, Mutation


class Planta(ObjectType):
    id = Int()
    nombre = String()
    especie = String()
    edad = Int()
    altura = Int()
    frutos = Boolean()

class Query(ObjectType):
    plantas   = List(Planta)
    plantas_por_id = Field(Planta, id=Int())
    buscar_plantas_por_especie = List(Planta, especie=String())
    buscar_plantas_por_frutos = List(Planta)
    
    def resolve_plantas(root, info):        
        return plantas
    
    def resolve_plantas_por_id(root, info, id):
        for planta in plantas:
            if planta.id == id:
                return planta
        return None    

    def resolve_buscar_plantas_por_especie(root, info, especie):
        return [planta for planta in plantas if planta.especie == especie]
    
    def resolve_buscar_plantas_por_frutos(root, info):
        return [planta for planta in plantas if planta.frutos == True]

class CrearPlanta(Mutation):
    class Arguments:
        nombre = String()
        especie = String()
        edad = Int()
        altura = Int()
        frutos = Boolean()

    planta = Field(Planta)
    
    def mutate(root, info, nombre, especie, edad, altura,frutos):
        nuevo_planta = Planta(
            id=len(plantas) + 1, 
            nombre=nombre, 
            especie=especie, 
            edad=edad,
            altura=altura,
            frutos=frutos
        )      
        
        plantas.append(nuevo_planta)
        print("Nueva planta creada:")
        return CrearPlanta(planta=nuevo_planta)

class DeletePlanta(Mutation):
    class Arguments:
        id = Int()

    planta = Field(Planta)

    def mutate(root, info, id):
        for i, planta in enumerate(plantas):
            if planta.id == id:
                plantas.pop(i)
                return DeletePlanta(planta=planta)
        return None
    
class UpdatePlanta(Mutation):
    class Arguments:
        id = Int()
        nombre = String(required=False)
        especie = String(required=False)
        edad = Int(required=False)
        altura = Int(required=False)
        frutos = Boolean(required=False)

    planta = Field(Planta)

    def mutate(root, info, id, **kwargs):
        for planta in plantas:
            if planta.id == id:
                for key, value in kwargs.items():
                    setattr(planta, key, value)
                return UpdatePlanta(planta=planta)
        return None

class Mutations(ObjectType):
    crear_planta = CrearPlanta.Field()
    delete_planta = DeletePlanta.Field()
    update_planta = UpdatePlanta.Field()

plantas = [
    Planta(id=1, nombre="rosa", especie="rosa", edad=15, altura=30, frutos=False),
    Planta(id=2, nombre="girasol", especie="girasol", edad=20, altura=50, frutos=True),
    Planta(id=3, nombre="lirio", especie="lirio", edad=10, altura=25, frutos=False),
    Planta(id=4, nombre="tulipán", especie="lirio", edad=8, altura=20, frutos=False),
    Planta(id=5, nombre="margarita", especie="girasol", edad=12, altura=35, frutos=False),
]

schema = Schema(query=Query, mutation=Mutations)

class GraphQLRequestHandler(BaseHTTPRequestHandler):
    def response_handler(self, status, data):
        self.send_response(status)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_POST(self):
        if self.path == "/graphql":
            content_length = int(self.headers["Content-Length"])
            data = self.rfile.read(content_length)
            data = json.loads(data.decode("utf-8"))
            print(data)
            result = schema.execute(data["query"])
            self.response_handler(200, result.data)
        else:
            self.response_handler(404, {"Error": "Ruta no existente"})

def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, GraphQLRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()

if __name__ == "__main__":
    run_server()
