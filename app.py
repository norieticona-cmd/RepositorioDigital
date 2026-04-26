import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from models import db, Documento, Usuario

app = Flask(__name__)

# Configuración de BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///repositorio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración de subida de archivos
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/admin')
def admin():
    documentos = Documento.query.all()
    usuarios = Usuario.query.all()
    return render_template('admin.html', documentos=documentos, usuarios=usuarios)

@app.route('/registrar', methods=['POST'])
def registrar_documento():
    titulo = request.form['titulo']
    categoria = request.form['categoria']
    fecha = request.form['fecha']

    archivo = request.files['archivo']
    nombre_seguro = secure_filename(archivo.filename)
    ruta_archivo = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
    archivo.save(ruta_archivo)

    nuevo_doc = Documento(
        titulo=titulo,
        categoria=categoria,
        fecha=fecha,
        archivo=nombre_seguro
    )
    db.session.add(nuevo_doc)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/uploads/<filename>')
def descargar_archivo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# 🔎 Ruta de búsqueda
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    resultados = []
    if request.method == 'POST':
        termino = request.form['termino']
        resultados = Documento.query.filter(Documento.titulo.contains(termino)).all()
    return render_template('buscar.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
