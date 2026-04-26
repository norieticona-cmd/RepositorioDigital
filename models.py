from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Documento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.String(20), nullable=False)
    archivo = db.Column(db.String(200), nullable=False)  # nombre del archivo

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    rol = db.Column(db.String(50), nullable=False)
