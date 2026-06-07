#Desde Flask vamos a importar Blueprint, que sirve para imprimir nuestras rutas, render_template que las renderiza, request que
#pide datos y url for que une nuestras rutas.
from flask import Blueprint, render_template, request, redirect, url_for
#SIEMPRE tenemos que llamar a la conexión con MongoDB. 
from database import db


citas_bp = Blueprint('citas', __name__)
#Este es el nombre de la colección dentro de la base de datos. 
col = db['citas']

#Aquí hacemos la primera ruta, todo lo que tenga arroba al principio es una ruta. 
@citas_bp.route("/")
#Esta es una función que nos ayudará a imprimir nuestros registros, es por ello que nos regresa un renderizado de nuestros registros. 
def ver_citas():
    lista = list(col.find())
    return render_template('citas.html', citas=lista)

#Ahora vamos a renderizar nuestro formulario mediante esta ruta, y esta función. 
#Los nombres de las rutas son importantes porque las necesitamos para llamarlas después. 
@citas_bp.route("/nueva")
def formulario():
    return render_template('formcitas.html')
    #Aquí se llama al formulario, que está dentro de otro archivo HTML. 


#Esta es nuestra ruta para guardar nuevos registros. 
#POST siempre significa agregado, o integrar a algo. 

@citas_bp.route("/guardar", methods=["POST"])
#Esta es la función donde vamos a almacenar los datos.
#Yo tengo este revoltijo raro para que los IDS de los empleados, citas o pacientes sean automáticos dependiendo del número de registros previos.

def guardar():
    ultimo = col.find_one(sort=[("id_cita", -1)])
    nuevo_id = (ultimo["id_cita"] + 1) if ultimo else 1
    #Estos son los requerimientos de mis registros, que los vamos a insertar en la colección. 
    col.insert_one({
    "id_cita":  nuevo_id,
    "paciente": request.form.get("paciente"),
    "medico":   request.form.get("medico"),
    "fecha":    request.form.get("fecha"),
    "motivo":   request.form.get("motivo"),
    "estatus":  request.form.get("estatus"),
})
    return redirect(url_for('citas.ver_citas'))
    #Y finalmente nos redirije a la página principal donde estan almacenadas todas las citas. 