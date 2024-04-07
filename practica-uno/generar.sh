#!/bin/bash

# Creacion de la estructura de carpetas
mkdir -p ./ejercicio-{uno,dos,tres,cuatro,cinco,seis,siete,ocho}

# Creacion de los archivos
touch ./ejercicio-uno/{soap_server.py,soap_client.py}
touch ./ejercicio-dos/{gql_server.py,gql_client.py}
touch ./ejercicio-tres/{rest_server.py,rest_client.py}
touch ./ejercicio-cuatro/{builder_server.py,builder_client.py}
touch ./ejercicio-cinco/{rest_server.py,rest_client.py}
touch ./ejercicio-seis/{factory_server.py,factory_client.py}
touch ./ejercicio-siete/{singleton_server.py,singleton_client.py}
touch ./ejercicio-ocho/{cesar_server.py,cesar_client.py}

# mensaje feliz cuando cuando termine en exito
echo "¡Estructura de carpetas y archivos creada exitosamente! :)"
