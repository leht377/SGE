from flask import Flask, render_template, redirect, request, session
import os
from flask.helpers import url_for
from flask_wtf import form
from werkzeug.security import check_password_hash, generate_password_hash
from formularios import form_loginSGE, form_search
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
        cur.execute("SELECT id FROM datos_de_usuario WHERE usuario = %s and contrasena = %s", (User, Passw))
        id = cur.fetchone()

        if id != None:
            session['Usuario'] = True
            cur.execute("SELECT empleado.cedula, empleado.nombre,empleado.apellido,empleado.rol_id,rol.rol FROM empleado,rol WHERE empleado.cedula = %s and empleado.rol_id = rol.id;", (id))
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
        return render_template('baseDashboard.html', form=form, informacion=informacion)
    else:
        return redirect('/')

@app.route('/Dashboard/informacion_personal', methods=["GET", "POST"])
def informacionPersonal():
    if "Usuario" in session:
        global informacion
        form = form_search()
        cur = mysql.connection.cursor()
        cur.execute("SELECT empleado.cedula,empleado.nombre,empleado.apellido,empleado.telefono,empleado.salario,empleado.dependencia ,datos_de_usuario.usuario, informacioncontrato.fecha_ingreso,informacioncontrato.fecha_terminacion,informacioncontrato.tipoContrato,rol.rol FROM empleado,informacioncontrato,datos_de_usuario,rol WHERE empleado.cedula = %s and empleado.datos_de_usuario_id =  datos_de_usuario.id and informacioncontrato.empleado_cedula = empleado.cedula and empleado.rol_id = rol.id;",(informacion[0],))
        datosUsuario = cur.fetchall()[0]
        return render_template('includes/informacionPersonal.html', form=form, informacion=informacion,datosUsuario=datosUsuario)
    else:
        return redirect('/')
# POR HACER

@app.route('/Dashboard/ver_retroalimentacion', methods=["GET", "POST"])
def ver_retroalimentacion():
    if "Usuario" in session:
        global informacion
        form = form_search()
        return render_template('includes/verRetroalimentacion.html', form=form, informacion=informacion)
    else:
        return redirect('/')


@app.route('/Dashboard/lista_empleados', methods=["GET", "POST"])
def listar_empleados():
    if "Usuario" in session:
        global informacion
        form = form_search()
        return render_template('includes/listarEmpleados.html', form=form, informacion=informacion)
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
