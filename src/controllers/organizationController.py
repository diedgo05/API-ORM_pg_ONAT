from flask import jsonify, request, send_file
from src.models.organizations import Organizations
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models import db
from config import drive_service
from src.controllers.driveController import upload_to_drive, download_from_drive
from io import BytesIO
import tempfile, os

# Modificación en crear una organización para permitir consultas en postman o thunderclient con form-data
def crear_org():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    cp = request.form.get('cp')
    estado = request.form.get('estado')
    municipio = request.form.get('municipio')
    colonia = request.form.get('colonia')
    direccion = request.form.get('direccion')
    rfc = request.form.get('rfc')
    telefono = request.form.get('telefono')
    contrasena = request.form.get('contrasena')
    imagen = request.form.get('imagen')

    if not nombre:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if Organizations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya está registrado"}), 400

    if not imagen:
        return jsonify({"mensaje": "Falta la imagen"}), 400


    nueva_org = Organizations(
        nombre=nombre,
        correo=correo,
        cp=cp,
        estado=estado,
        municipio=municipio,
        colonia=colonia,
        direccion=direccion,
        rfc=rfc,
        telefono=telefono,
        contrasena=contrasena,
        imagen=imagen  
    )
    
    db.session.add(nueva_org)
    db.session.commit()

    return jsonify({
        "mensaje": "Organización creada",
        "id": nueva_org.id,
        "imagen_drive_id": nueva_org.imagen
    }), 201

def login_organizacion(data):
    try:
        correo = data.get('correo')
        contrasena = data.get('contrasena')
        
        if not correo or not contrasena:
            return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
        
        organizacion = Organizations.query.filter_by(correo=correo).first()

        if not organizacion:
            return jsonify({"mensaje": "Credenciales inválidas"}), 401
        if not organizacion.check_contrasena(contrasena):
            return jsonify({"mensaje": "Credenciales inválidas"}), 401

        # Agregar log de depuración
        print(f"Usuario autenticado: {organizacion.id}, correo: {correo}")

        # Generar token
        access_token = create_access_token(identity=str(organizacion.id))
        return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200
    
    except Exception as e:
        print(f"Error en login_organizacion: {str(e)}")
        return jsonify({"error": "Error en el servidor", "detalle": str(e)}), 500
@jwt_required()
def obtener_organizaciones():
    try:
        organizaciones = Organizations.query.all()  
        if not organizaciones:
            return jsonify({"mensaje": "No se encontraron organizaciones"}), 404

        resultado = []
        for organizacion in organizaciones:
            resultado.append({
                "id": organizacion.id,
                "nombre": organizacion.nombre,
                "correo": organizacion.correo,
                "cp": organizacion.cp,
                "estado": organizacion.estado,
                "municipio": organizacion.municipio,
                "colonia": organizacion.colonia,
                "direccion": organizacion.direccion,
                "rfc": organizacion.rfc,
                "telefono": organizacion.telefono,
                "imagen": organizacion.imagen
            })

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": "Error procesando la solicitud", "detalle": str(e)}), 500

@jwt_required()
def actualizar_organizaciones(id, data):
    organizacion = Organizations.query.get(id)
    if not id:
        return jsonify({"mensaje":"No se puede editar esta organización"}), 403
    if not organizacion:
        return jsonify({"mensaje":" Organización benéfica no encontrada"}),404
    
    nombre = data.get('nombre')
    correo = data.get('correo')
    telefono = data.get('telefono')

    if nombre:
        organizacion.nombre = nombre
    if correo:
        if Organizations.query.filter_by(correo=correo).first() and organizacion.correo != correo:
            return jsonify({"mensaje":" El correo ya se encuentra en uso"}), 400
        organizacion.correo = correo
    if telefono:
        if Organizations.query.filter_by(telefono=telefono).first() and organizacion.telefono != telefono:
            return jsonify({"mensaje":" El número de teléfono ya esta en uso"}), 400
        organizacion.telefono = telefono
    
    db.session.commit()

    return jsonify({
        "id": organizacion.id,
        "nombre": organizacion.nombre,
        "correo": organizacion.correo,
        "cp": organizacion.cp,
        "estado": organizacion.estado,
        "municipio": organizacion.municipio,
        "colonia": organizacion.colonia,
        "direccion": organizacion.direccion,
        "rfc": organizacion.rfc,
        "telefono": organizacion.telefono,
        "imagen": organizacion.imagen
    }), 200

@jwt_required()
def eliminar_organizacion(id):
    organizacion = Organizations.query.get(id)
    if not organizacion:
        return jsonify({"mensaje":"Organización benéfica no encontrada"}), 404
    db.session.delete(organizacion)
    db.session.commit()
    return jsonify({"mensaje":"Organización eliminada correctamente"}), 200