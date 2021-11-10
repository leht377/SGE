from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators,SelectField
from wtforms.fields.html5 import DateField, EmailField,SearchField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class form_loginSGE(FlaskForm):
    Usuario = StringField('Usuario',validators=[DataRequired(message='No dejar el campo vacio')],render_kw={"placeholder": "Ingrese usuario"})
    contrasena = PasswordField('Contraseña', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')],render_kw={"placeholder": "Ingrese contraseña"})
    Sesion = SubmitField('Iniciar sesión')

class form_search(FlaskForm):
    search = SearchField('Buscar',render_kw={"placeholder": "Ingrese cedula"},id='searchEmpleado')

class form_crearEmpleado(FlaskForm):
    Cedula = StringField('Cedula',validators=[DataRequired(message='No dejar el campo vacio')],id='inputCedula')
    Nombre = StringField('Nombre',validators=[DataRequired(message='No dejar el campo vacio')],id='inputNombre')
    Apellido = StringField('Apellido',validators=[DataRequired(message='No dejar el campo vacio')])
    Telefono = StringField('Telefono',validators=[DataRequired(message='No dejar el campo vacio')])
    Salario = StringField('Salario',validators=[DataRequired(message='No dejar el campo vacio')])
    Dependecia = StringField('Dependecia',validators=[DataRequired(message='No dejar el campo vacio')])
    Fecha_ingreso = DateField('Fecha ingreso', format='%Y-%m-%d')
    Fecha_terminacion = DateField('Fecha terminacion', format='%Y-%m-%d')
    Tipo_contrato = StringField('Tipo contrato',validators=[DataRequired(message='No dejar el campo vacio')])
    Rol = SelectField("Rol: ",choices=[("Empleado"),("Administrador"),("SuperAdministrador")])
    Usuario = StringField('Usuario',validators=[DataRequired(message='No dejar el campo vacio')])
    contrasena = PasswordField('Contraseña', [validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    Guardar = SubmitField('Guardar',id='btnGuardarEmpleado')
