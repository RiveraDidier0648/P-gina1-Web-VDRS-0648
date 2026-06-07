from flask import Blueprint, render_template
from database import db

index_bp = Blueprint('index', __name__)

@index_bp.route("/")
def dashboard():
    total_pacientes = db['pacientes'].count_documents({})
    total_doctores  = db['doctores'].count_documents({})
    total_citas     = db['citas'].count_documents({})
    return render_template('index.html',
        total_pacientes=total_pacientes,
        total_doctores=total_doctores,
        total_citas=total_citas
    )