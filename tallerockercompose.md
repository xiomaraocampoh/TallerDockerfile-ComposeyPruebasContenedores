Parte 1 - La aplicacion
Cree una aplicacion pequena con las siguientes caracteristicas:

Al menos 3 endpoints o funciones expuestas (por ejemplo: crear, listar y eliminar un recurso)
Conexion a una base de datos (PostgreSQL, MySQL, MariaDB o MongoDB)
Al menos 3 pruebas unitarias que validen el comportamiento de los endpoints o funciones
La logica del negocio es libre. Puede ser una lista de tareas, un inventario, un registro de estudiantes, lo que prefiera.

Parte 2 - El Dockerfile
Escriba un Dockerfile para su aplicacion. Debe cumplir lo siguiente:

Partir de una imagen base oficial del lenguaje que eligio
Definir un directorio de trabajo dentro del contenedor
Copiar e instalar las dependencias antes de copiar el resto del codigo
Copiar el codigo de la aplicacion
Exponer el puerto que usa la aplicacion
Definir el comando que inicia la aplicacion
Construya la imagen y verifique que no hay errores:

docker build -t mi-app:v1 .
Verifique que la imagen aparece en:

docker images
Parte 3 - Docker Compose
Escriba un archivo docker-compose.yml que levante dos servicios: su aplicacion y la base de datos. Debe cumplir lo siguiente:

El servicio de la base de datos debe usar una imagen oficial y tener configuradas las variables de entorno necesarias (usuario, contrasena, nombre de la base de datos)
El servicio de la base de datos debe tener un volumen para persistir los datos
El servicio de la base de datos debe tener un healthcheck
El servicio de la aplicacion debe construirse desde su Dockerfile (no usar una imagen preexistente)
El servicio de la aplicacion debe recibir por variables de entorno los datos de conexion a la base de datos
El servicio de la aplicacion debe depender del servicio de base de datos y esperar a que este saludable antes de iniciar
Ambos servicios deben tener sus puertos mapeados al host
Levante los servicios:

docker compose up -d
Verifique que ambos estan corriendo:

docker compose ps
Verifique que la aplicacion responde haciendo una peticion al endpoint principal desde su maquina.

Parte 4 - Pruebas dentro del contenedor
Ejecute las pruebas unitarias dentro del contenedor de la aplicacion, sin instalar nada en su maquina:

docker compose exec <nombre-servicio> <comando-de-pruebas>
Tambien ejecutelas usando un contenedor temporal que se elimina al terminar:

docker compose run --rm <nombre-servicio> <comando-de-pruebas>
Verifique que todas las pruebas pasan. Si alguna falla, corrija el error y vuelva a ejecutarlas.

Parte 5 - Modificacion y reconstruccion
Agregue un endpoint o funcion adicional a su aplicacion y escriba al menos una prueba para ese nuevo comportamiento.

Reconstruya solo el servicio de la aplicacion sin detener la base de datos:

docker compose up -d --build <nombre-servicio>
Ejecute las pruebas de nuevo y verifique que todo sigue pasando.

Entregables
Codigo fuente de la aplicacion
Dockerfile
docker-compose.yml
Captura o salida del comando docker compose ps con ambos servicios corriendo
Captura o salida de las pruebas ejecutadas dentro del contenedor con todas pasando