# Servicio-API-REST_Flask
=========================================================================


## Description
------------------------------------
El servicio REST que deberás realizar tiene la funcionalidad de registrar y consultar usuarios, procesar archivos, además de contar con un control de acceso.
## Getting Started
---------------
### Prerequisites
* Tener Python instalado en tu máquina (versión 3.8 o superior)
    ```bash
        python -m venv name_virtual
    ```
* Tener pip instalado (el administrador de paquetes de Python)
### Installation
* 0.- Clona El Repositorio [Servicio-API-REST_Flask](https://github.com/wieneberMA/Servicio-API-REST_Flask)
* 1.- Abre una terminal o command prompt en la carpeta raíz del proyecto.
* 2.- Ejecuta el comando pip install -r requirements.txt para instalar todas las dependencias necesarias.
    ```python bash
        pip install -r requirements.txt
    ```
* 3.- Crea el **DB** y Configura el Archivo **config.py**
    ```python
        class Config:
            DB_USERNAME = 'root'
            DB_PASSWORD = ''
            DB_HOST = 'localhost'
            DB_NAME = 'db_users'
    ```
* 4.- Migra las Bases de Datos
    ```python
        python -m flask db migrate
        python -m flask db upgrade
    ```
* 5.- Correo el Projecto
    ```python
        python -m flask --app app --debug run
    ```
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

# Optimizacion
Supongamos que tienes una aplicación web que muestra el listado de empleados en varios
módulos. Cada vez que un usuario visita la página, la aplicación realiza una consulta a una
base de datos para obtener el listado. Esto está afectando negativamente al rendimiento de la
aplicación debido a la frecuencia de las consultas a la base de datos.
Tu tarea es proponer una refactorización en el código para que las consultas a la base de
datos se realicen sólo cuando la información de los empleados cambia, en lugar de cada vez
que un usuario visita la página. Proponer una solución que almacene en caché la lista de
productos y solo actualice la caché cuando se añade, modifica o elimina un producto.

## Implementación

[Caching](https://flask.palletsprojects.com/en/3.0.x/patterns/caching/)
Cuando su aplicación se ejecuta con lentitud, agregue algunos cachés. Bueno, al menos es la forma más fácil de acelerar las cosas. ¿Qué hace un caché? Digamos que tiene una función que tarda un tiempo en completarse, pero los resultados serían lo suficientemente buenos si tuvieran 5 minutos de antigüedad. Entonces, la idea es que realmente coloque el resultado de ese cálculo en un caché durante un tiempo.
Flask en sí no proporciona almacenamiento en caché, pero Flask-Caching , una extensión para Flask, sí lo hace. Flask-Caching admite varios backends e incluso es posible desarrollar su propio backend de almacenamiento en caché.


* Utiliza una técnica de caching (almacenamiento en caché) para reducir el número de consultas a la base de datos. Esta solución se basa en la utilización de una librería de caching como Flask-Cache.

[Flask-Caching](https://flask-caching.readthedocs.io/en/latest/)
    ```python
        pip install Flask-Caching 
    ```

### Configuración  de Ejemplo
* **app.py**
    ```python
        from flask import Flask
        from flask_cache import Cache

        app = Flask(__name__)
        cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'}) 

        @cache.cached(timeout=60)  # caching for 1 minute
        def get_employees():
            employees = Employee.query.all()
            return [employee.to_dict() for employee in employees]

        @app.route('/employees')
        def show_employees():
            employees = get_employees()
            return render_template('employees.html', employees=employees)

        @cache.memoize(timeout=60)
        def add_employee(employee):
            db.session.add(employee)
            db.session.commit()
            cache.delete_memoized(get_employees)

        @cache.memoize(timeout=60)
        def update_employee(employee):
            db.session.commit()
            cache.delete_memoized(get_employees)

        @cache.memoize(timeout=60)
        def delete_employee(employee):
            db.session.delete(employee)
            db.session.commit()
            cache.delete_memoized(get_employees)
    ```

En estos ejemplos, estamos utilizando la función @cache.memoize para indicar que las funciones add_employee, update_employee y delete_employee deben actualizar la caché después de realizar cada una de estas operaciones.