from flask import Flask, render_template, redirect, request
import os
from flask_wtf import form
from werkzeug.security import check_password_hash, generate_password_hash
from formularios import form_loginSGE, form_search
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = os.urandom(24)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'nacional2015'
app.config['MYSQL_DB'] = 'sge'
mysql = MySQL(app)

informacion = ''


@app.route('/', methods=["GET"])
def inicio():
    form = form_loginSGE()
    return render_template('login.html', form=form)


@app.route('/Dashboard', methods=["GET", "POST"])
def dashboard():
    if request.method == 'POST':
        global informacion
        form = form_loginSGE()
        User = form.Usuario.data
        Passw = form.contrasena.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM datos_de_usuario WHERE usuario = %s and contrasena = %s", (User, Passw))
        id = cur.fetchone()

        if id != None:
            cur.execute("SELECT empleado.cedula, empleado.nombre,empleado.apellido,empleado.rol_id,rol.rol FROM empleado,rol WHERE empleado.cedula = %s and empleado.rol_id = rol.id;", (id))
            informacion = cur.fetchall()[0]
            cur.close()
            mysql.connection.commit()
            form = form_search()
            return render_template('baseDashboard.html', form=form, informacion=informacion)
    else:
        redirect('/')

# POR HACER


@app.route('/Dashboard/informacion_personal', methods=["GET", "POST"])
def informacionPersonal():
    global informacion
    form = form_search()
    cur = mysql.connection.cursor()
    cur.execute("SELECT empleado.cedula,empleado.nombre,empleado.apellido,empleado.telefono,empleado.salario,empleado.dependencia ,datos_de_usuario.usuario, informacioncontrato.fecha_ingreso,informacioncontrato.fecha_terminacion,informacioncontrato.tipoContrato,rol.rol FROM empleado,informacioncontrato,datos_de_usuario,rol WHERE empleado.cedula = %s and empleado.datos_de_usuario_id =  datos_de_usuario.id and informacioncontrato.empleado_cedula = empleado.cedula and empleado.rol_id = rol.id;",(informacion[0],))
    datosUsuario = cur.fetchall()[0]
    return render_template('includes/informacionPersonal.html', form=form, informacion=informacion,datosUsuario=datosUsuario)


@app.route('/Dashboard/ver_retroalimentacion', methods=["GET", "POST"])
def ver_retroalimentacion():
    global informacion
    form = form_search()
    return render_template('includes/verRetroalimentacion.html', form=form, informacion=informacion)


@app.route('/Dashboard/lista_empleados', methods=["GET", "POST"])
def listar_empleados():
    global informacion
    form = form_search()
    return render_template('includes/listarEmpleados.html', form=form, informacion=informacion)


if __name__ == "__main__":
    app.run(debug=True)
