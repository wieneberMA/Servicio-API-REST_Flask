from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from flask import jsonify
from flask_login import LoginManager, UserMixin, login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask import flash
# archivos
from flask import send_file
import os
import csv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SECRET_KEY'] = '1q2w3e4r5t6y7u8i9o0p'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'Archivos')
ALLOWED_EXTENSIONS = {'csv'}

db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import User

##Validaciones
def email_validacion(email):
    existing_user = User.query.filter_by(email=email).first()
    return existing_user is not None


def validate_password(password):
    """
    Valida la contraseña según los siguientes criterios:
    - Debe tener al menos 8 caracteres
    - Debe contener al menos una letra mayúscula
    - Debe contener al menos una letra minúscula
    - Debe contener al menos un número
    - Debe contener al menos un carácter especial (!, @, #, $, etc.)
    """
    if len(password) < 8:
        return {"error": "La contraseña debe tener al menos 8 caracteres"}
    if not any(char.isupper() for char in password):
        return {"error": "La contraseña debe contener al menos una letra mayúscula"}
    if not any(char.islower() for char in password):
        return {"error": "La contraseña debe contener al menos una letra minúscula"}
    if not any(char.isdigit() for char in password):
        return {"error": "La contraseña debe contener al menos un número"}
    if not any(char in '!@#$%^&*()-+?_=,<>/~`|\\' for char in password):
        return {"error": "La contraseña debe contener al menos un carácter especial"}
    return {"success": "La contraseña es válida"}


login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

jwt = JWTManager(app)

@app.route('/')
def index():
    return redirect(url_for('show_login'))

@app.route('/protected')
@jwt_required
def protected():
    return 'Acceso permitido'

@app.route('/users')
# @jwt_required
def get_users():
    users = User.query.all()
    nombre = request.args.get('nombre')
    estado = request.args.get('estado')

    if nombre:
        users = User.query.filter(
            (User.nombre.like(f"%{nombre}%")) |
            (User.apellido_paterno.like(f"%{nombre}%")) |
            (User.apellido_materno.like(f"%{nombre}%"))
        ).all()
    if estado:
        users = User.query.filter(User.is_active == (estado == "True")).all()

    return render_template("Users_list.html", users=users)


@app.route('/login', methods=["GET", "POST"])
def show_login():
    if request.method == 'POST':
        useremail = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=useremail).first()
        if user and check_password_hash(user.password, password):
            # User exists and password is correct, login successful
            access_token = create_access_token(identity=user.email)
            print(f"Acces Token:{access_token}" )
            jsonify(access_token=access_token), 200
            return redirect(url_for('get_users'))
        else:
            # Invalid credentials
            error = 'Correo o Contraseña No valido'
            return render_template("login.html", error=error, token_denied=True), 401
    return render_template("login.html")

@app.route("/registro/", methods=["GET", "POST"])
def show_signup_form():
    from forms import SignupForm
    if request.method == "GET":
        form = SignupForm()
    else:
        form = SignupForm(request.form)
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        password_validation = validate_password(password)
        if "error" in password_validation:
            error = password_validation["error"]
            return render_template("form_registro.html", form=form, error=error)
        if email_validacion(email):
            # El correo electrónico ya existe, mostrar un mensaje de error
            error = 'El correo electrónico ya existe'
            return render_template("form_registro.html", form=form, error=error)
        else:
            user = User(
                nombre=form.nombre.data,
                apellido_paterno=form.apellido_paterno.data,
                apellido_materno=form.apellido_materno.data,
                fecha_nacimiento=form.fecha_nacimiento.data,
                nickname=form.nickname.data,
                email=form.email.data,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                is_active=True
            )
            db.session.add(user)
            db.session.commit()
            flash("Cuenta Creada")
            return redirect(url_for('show_login'))
    return render_template("form_registro.html", form=form)


@app.route("/salarios")
def show_salarios():
    return render_template("carga_salarios.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            extension = filename.split('.')[-1].lower()
            if extension in ALLOWED_EXTENSIONS:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',', quotechar='"')  # Utiliza la coma como delimitador
                    next(reader)  # Saltarte la primera fila del archivo CSV
                    datos = [row for row in reader]  # Asegúrate de que datos sea una lista de listas

                    # Procesar los datos para calcular el salario promedio y el empleado con el salario más alto
                    salarios = []
                    for row in datos:
                        if len(row) > 1:  # Asegúrate de que la fila tenga al menos dos columnas
                            nombre = row[0]
                            salario = float(row[1])  # Asumimos que el salario es el segundo elemento de la fila
                            salarios.append((nombre, salario))

                    if salarios:
                        salario_promedio = sum(salario for _, salario in salarios) / len(salarios)
                        empleado_mas_alto = max(salarios, key=lambda x: x[1])

                        msj = 'Archivo cargado'
                        return render_template("carga_salarios.html", msj=msj, Data=datos, salario_promedio=salario_promedio, empleado_mas_alto=empleado_mas_alto)
                    else:
                        msj = 'No se encontraron datos válidos en el archivo'
                        return render_template("carga_salarios.html", msj=msj, Data=datos)
            else:
                return 'La extensión del archivo no está permitida', 400
        else:
            return 'No se ha seleccionado ningún archivo', 400
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
