from flask import Flask, render_template, redirect, request, session
import os
from flask.helpers import url_for
from flask_wtf import form
from werkzeug.security import check_password_hash, generate_password_hash
from formularios import form_loginSGE, form_search, form_crearEmpleado
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = os.urandom(24)

# Solo para detectar cambios
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nacional2015'
app.config['MYSQL_DB'] = 'sge'

mysql = MySQL(app)

informacion = ''
roldiccionario = {
    'Empleado':1,
    'Administrador':2,
    'SuperAdministrador':3
}

@app.route('/', methods=["GET"])
def inicio():
    form = form_loginSGE()
    return render_template('login.html', form=form)

@app.route('/ingreso', methods = ["POST"]) #aca se valida el usuario
def ingreso():
     if request.method == 'POST':
        global informacion

        form = form_loginSGE()
        User = form.Usuario.data
        Passw = form.contrasena.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT id,contrasena FROM datos_de_usuario WHERE usuario = %s", (User,))
        dataUser = cur.fetchone()

        if id != None and check_password_hash(dataUser[1],Passw):
            session['Usuario'] = True
            cur.execute("SELECT empleado.cedula, empleado.nombre,empleado.apellido,empleado.rol_id,rol.rol FROM empleado,rol WHERE empleado.cedula = %s and empleado.rol_id = rol.id;", (dataUser[0],))
            informacion = cur.fetchall()[0]
            cur.close()
            mysql.connection.commit()
            return redirect('/Dashboard')
        else:
            return redirect('/')

@app.route('/Dashboard', methods=["GET", "POST"])
def dashboard():
    if "Usuario" in session:
        global informacion
        form = form_search()
        formModal = form_crearEmpleado()
        return render_template('baseDashboard.html', form=form, informacion=informacion,formModal=formModal)
    else:
        return redirect('/')

@app.route('/Dashboard/informacion_personal', methods=["GET", "POST"])
def informacionPersonal():
    if "Usuario" in session:
        global informacion
        form = form_search()
        formModal = form_crearEmpleado()
        cur = mysql.connection.cursor()
        cur.execute("SELECT empleado.cedula,empleado.nombre,empleado.apellido,empleado.telefono,empleado.salario,empleado.dependencia ,datos_de_usuario.usuario, informacioncontrato.fecha_ingreso,informacioncontrato.fecha_terminacion,informacioncontrato.tipoContrato,rol.rol FROM empleado,informacioncontrato,datos_de_usuario,rol WHERE empleado.cedula = %s and empleado.datos_de_usuario_id =  datos_de_usuario.id and informacioncontrato.empleado_cedula = empleado.cedula and empleado.rol_id = rol.id;",(informacion[0],))
        datosUsuario = cur.fetchall()[0]
        return render_template('includes/informacionPersonal.html', form=form, informacion=informacion,datosUsuario=datosUsuario,formModal=formModal)
    else:
        return redirect('/')
# POR HACER

@app.route('/CrearEmpleado', methods=["GET", "POST"])
def crearEmpleado():
    if "Usuario" in session and request.method == 'POST':
        global informacion
        formModal = form_crearEmpleado()
        cedula = formModal.Cedula.data
        nombre = formModal.Nombre.data
        apellido = formModal.Apellido.data
        telefono = formModal.Telefono.data
        salario = formModal.Salario.data
        dependencia =formModal.Dependecia.data
        fecha_ingreso = formModal.Fecha_ingreso.data
        fecha_terminacion = formModal.Fecha_terminacion.data
        tipo_contrato = formModal.Tipo_contrato.data
        rol= formModal.Rol.data
        usuario = formModal.Usuario.data
        contrasena = formModal.contrasena.data
        passwordIncritp = generate_password_hash(contrasena)

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO datos_de_usuario (id,usuario,contrasena) VALUES (%s,%s,%s)',(cedula,usuario,passwordIncritp))
        cur.execute('INSERT INTO empleado (cedula,nombre,apellido,telefono,salario,dependencia,rol_id,datos_de_usuario_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(cedula,nombre,apellido,telefono,salario,dependencia,roldiccionario[rol],cedula))
        cur.execute('INSERT INTO informacioncontrato (fecha_ingreso,fecha_terminacion,tipoContrato,empleado_cedula) VALUES (%s,%s,%s,%s)',(fecha_ingreso,fecha_terminacion,tipo_contrato,cedula))
        
        mysql.connection.commit()
        mysql.connection.close()

        return redirect('/Dashboard')
    else:
        return redirect('/')


@app.route('/Dashboard/ver_retroalimentacion', methods=["GET", "POST"])
def ver_retroalimentacion():
    if "Usuario" in session:
        global informacion
        form = form_search()
        formModal = form_crearEmpleado()
        return render_template('includes/verRetroalimentacion.html', form=form, informacion=informacion,formModal=formModal)
    else:
        return redirect('/')


@app.route('/Dashboard/lista_empleados', methods=["GET", "POST"])
def listar_empleados():
    if "Usuario" in session:
        global informacion
        formModal = form_crearEmpleado()
        form = form_search()
        return render_template('includes/listarEmpleados.html', form=form, informacion=informacion,formModal=formModal)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    if "Usuario" in session:
        session.pop("Usuario",None)
        return redirect('/')
    else:
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
