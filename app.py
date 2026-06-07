# Flask backend para Didi's pet care
from flask import Flask, render_template, request, redirect, url_for, abort
from bson.objectid import ObjectId
from database import db
from routes.index import index_bp
from routes.pacientes import pacientes_bp
from routes.doctores import doctores_bp
from routes.citas import citas_bp

app = Flask(__name__, template_folder='templates', static_folder='static')

ADMIN_PASSWORD = 'didi1234'
allowed_collections = {
    'personal': 'personal',
    'mascotas': 'mascotas',
    'inventario': 'inventario',
}

app.register_blueprint(index_bp)
app.register_blueprint(pacientes_bp, url_prefix='/pacientes')
app.register_blueprint(doctores_bp, url_prefix='/doctores')
app.register_blueprint(citas_bp, url_prefix='/citas')

@app.route('/')
@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/inicio.html')
def inicio_page():
    return render_template('inicio.html')

@app.route('/personal.html')
def personal_page():
    personal = list(db['personal'].find({}))
    return render_template('personal.html', personal=personal)

@app.route('/mascotas.html')
def mascotas_page():
    mascotas = list(db['mascotas'].find({}))
    return render_template('mascotas.html', mascotas=mascotas)

@app.route('/inventario.html')
def inventario_page():
    inventario = list(db['inventario'].find({}))
    return render_template('Inventario.html', inventario=inventario)

def get_redirect_endpoint(tipo):
    page_endpoints = {
        'personal': 'personal_page',
        'mascotas': 'mascotas_page',
        'inventario': 'inventario_page',
    }
    return page_endpoints.get(tipo, 'home')

@app.route('/add', methods=['POST'])
def add_record():
    tipo = request.form.get('tipo')
    if tipo not in allowed_collections:
        return 'Tipo de registro no válido.', 400

    data = {key: value for key, value in request.form.items() if key != 'tipo'}
    data['creado'] = request.form.get('creado') or None

    collection = db[allowed_collections[tipo]]
    collection.insert_one(data)
    return redirect(url_for(get_redirect_endpoint(tipo)))

@app.route('/edit', methods=['POST'])
def edit_record():
    tipo = request.form.get('tipo')
    password = request.form.get('password')
    record_id = request.form.get('id')

    if password != ADMIN_PASSWORD:
        return 'Contraseña incorrecta.', 403
    if tipo not in allowed_collections:
        return 'Tipo de registro no válido.', 400
    if not record_id:
        return 'ID del documento requerido.', 400

    try:
        query_id = ObjectId(record_id)
    except Exception:
        return 'ID de documento inválido.', 400

    updates = {key: value for key, value in request.form.items() if key not in {'tipo', 'password', 'id'} and value}
    if not updates:
        return 'No se proporcionaron datos para actualizar.', 400

    collection = db[allowed_collections[tipo]]
    result = collection.update_one({'_id': query_id}, {'$set': updates})
    if result.matched_count == 0:
        return 'No se encontró el registro.', 404

    return redirect(url_for(get_redirect_endpoint(tipo)))

@app.route('/delete', methods=['POST'])
def delete_record():
    tipo = request.form.get('tipo')
    password = request.form.get('password')
    record_id = request.form.get('id')

    if password != ADMIN_PASSWORD:
        return 'Contraseña incorrecta.', 403
    if tipo not in allowed_collections:
        return 'Tipo de registro no válido.', 400
    if not record_id:
        return 'ID del documento requerido.', 400

    try:
        query_id = ObjectId(record_id)
    except Exception:
        return 'ID de documento inválido.', 400

    collection = db[allowed_collections[tipo]]
    result = collection.delete_one({'_id': query_id})
    if result.deleted_count == 0:
        return 'No se encontró el registro para borrar.', 404

    return redirect(url_for(get_redirect_endpoint(tipo)))

if __name__ == '__main__':
    app.run(debug=True)
