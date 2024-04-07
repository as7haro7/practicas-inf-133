from http.server import HTTPServer
from pysimplesoap.server import SoapDispatcher, SOAPHandler

# Define la función del servicio
def sumar(a,b):
    return a + b

def restar(a,b):
    return a - b

def multiplicar(a,b):
    return a * b

def dividir(a,b):
    return a / b

# Creamos la ruta del servidor SOAP
dispatcher = SoapDispatcher(
    "ejemplo-soap-server",
    location="http://localhost:8000/",
    action="http://localhost:8000/",
    namespace="http://localhost:8000/",
    trace=True,
    ns=True,
)

# Registramos el servicio
dispatcher.register_function(
    "Sumar",
    sumar,
    returns={"resultado": float},
    args={"a":float, "b":float},
)

dispatcher.register_function(
    "Restar",
    restar,
    returns={"resultado": float},
    args={"a":float, "b":float},
)


dispatcher.register_function(
    "Multiplicar",
    multiplicar,
    returns={"resultado": float},
    args={"a":float, "b":float},
)


dispatcher.register_function(
    "Dividir",
    dividir,
    returns={"resultado": float},
    args={"a":float, "b":float},
)


# Iniciamos el servidor HTTP
server = HTTPServer(("0.0.0.0", 8000), SOAPHandler)
server.dispatcher = dispatcher
print("Servidor SOAP iniciado en http://localhost:8000/")
server.serve_forever()
