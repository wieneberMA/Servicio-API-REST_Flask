# Servicio-API-REST_Flask
=========================================================================


## Description
------------------------------------
El servicio REST que deberás realizar tiene la funcionalidad de registrar y consultar usuarios, procesar archivos, además de contar con un control de acceso.
## Getting Started
---------------
### Prerequisites
### Installation
## Setup
## License
-------
## Authors
-------
### Personal Document
* **Wieneber macias ansurez** (Lead Developer) - [wieneber76@gmail.com](wieneber76@gmail.com)
## Acknowledgments
---------------
Este proyecto utiliza las siguientes bibliotecas y herramientas de terceros:

* Flask: Un microframework web de Python para construir aplicaciones web.
* Werkzeug: Una biblioteca de utilidades para aplicaciones web de Python.
* Flask-JWT-Extended: Una biblioteca para trabajar con tokens JSON Web Tokens (JWT) en Flask.
* Flask-Login: Una biblioteca para manejar la autenticación y autorización en Flask.
* Flask-SQLAlchemy: Una biblioteca para interactuar con bases de datos relacionales en Flask.
* Flask-Migrate: Una biblioteca para manejar las migraciones de la base de datos en Flask.
* CSV: Una biblioteca para leer y escribir archivos CSV.

* Además, agradezco a los desarrolladores y contribuidores de estas bibliotecas y herramientas por su trabajo y dedicación.
## What is Flask?
* Flask es un marco de desarrollo web de código abierto, escrito en Python. Fue diseñado para ser un marco minimalista, flexible y fácil de usar para la creación de aplicaciones web. 
Proporciona una manera sencilla de crear y desplegar aplicaciones web dinámicas; permite que los desarrolladores se centren en la lógica de la aplicación en lugar de que se preocupen por la infraestructura subyacente. Asimismo, ofrece una gran cantidad de libertad y control sobre el desarrollo de la aplicación, lo que lo vuelve ideal para proyectos pequeños y medianos. 

### Aplicación Web con Flask

* Este es un proyecto de aplicación web desarrollado con Flask, un microframework web de Python. La aplicación utiliza varias bibliotecas y herramientas de terceros, como Werkzeug, Flask-JWT-Extended, Flask-Login, Flask-SQLAlchemy, Flask-Migrate y CSV.

## Repository history
----------------
### Configuración de la Aplicación

La aplicación se configura con una serie de variables de entorno y configuraciones, como la cadena de conexión a la base de datos, la clave secreta para la autenticación JWT, la clave secreta para la sesión de Flask, y la carpeta de carga de archivos.

### Rutas de la Aplicación

La aplicación tiene varias rutas definidas:

* /: La ruta raíz que redirige al usuario a la página de inicio de sesión.
* /protected: Una ruta protegida que requiere autenticación JWT para acceder.
* /users: Una ruta que devuelve una lista de usuarios registrados en la base de datos. La ruta admite parámetros de consulta para filtrar los usuarios por nombre o estado.
* /login: La ruta de inicio de sesión que maneja la autenticación de usuarios.
* /registro/: La ruta de registro de usuarios que maneja la creación de nuevos usuarios.
* /salarios: La ruta que muestra la página de carga de salarios.
* /upload: La ruta que maneja la carga de archivos CSV. 

### Funcionalidades

La aplicación tiene varias funcionalidades:

* Autenticación de usuarios con JWT y Flask-Login.
* Registro de usuarios con Flask-WTF.
* Carga de archivos CSV y procesamiento de datos para calcular el salario promedio y el empleado con el salario más alto.
* Protección de rutas con autenticación JWT.
* Modelos
* La aplicación utiliza un modelo de usuario definido en el archivo models.py. El modelo de usuario tiene varios campos, como nombre, apellido paterno, apellido materno, fecha de nacimiento, nickname, email y contraseña.

### Formularios

* La aplicación utiliza formularios definidos con Flask-WTF para manejar la entrada de datos del usuario. El formulario de registro de usuarios tiene campos para nombre, apellido paterno, apellido materno, fecha de nacimiento, nickname, email y contraseña.

### Base de Datos

* La aplicación utiliza una base de datos relacional con SQLAlchemy para almacenar los datos de los usuarios. La base de datos se configura con una cadena de conexión que se establece en el archivo config.py.