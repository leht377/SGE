from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators
from wtforms.fields.html5 import EmailField,SearchField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class form_loginSGE(FlaskForm):
    Usuario = StringField('Usuario',validators=[DataRequired(message='No dejar el campo vacio')],render_kw={"placeholder": "Ingrese usuario"})
    contrasena = PasswordField('Contraseña', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')],render_kw={"placeholder": "Ingrese contraseña"})
    Sesion = SubmitField('Iniciar sesión')

class form_search(FlaskForm):
    search = SearchField('Buscar',render_kw={"placeholder": "Ingrese cedula"},id='searchEmpleado')