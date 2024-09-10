from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class SignupForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=100)])
    apellido_paterno = StringField('Apellido Paterno', validators=[DataRequired(), Length(min=2, max=100)])
    apellido_materno = StringField('Apellido Materno', validators=[DataRequired(), Length(min=2, max=100)])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Registrarse')