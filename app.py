from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@{Config.DB_HOST}/{Config.DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SECRET_KEY'] = '1q2w3e4r5t6y7u8i9o0p'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import User

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
    form = SignupForm()
    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellido_paterno=form.apellido_paterno.data,
            apellido_materno=form.apellido_materno.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            nickname=form.nickname.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data, method='pbkdf2:sha256')
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("form_registro.html", form=form)