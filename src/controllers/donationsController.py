from flask import jsonify
from src.models.donations import Donations, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@jwt_required()
def crear_donacion(data):
    nombre = data.get('nombre')
    apellido_m = data.get('apellido_m')
    apellido_p = data.get('apellido_p')
    correo = data.get('correo')
    nacionalidad = data.get('nacionalidad')
    cantidad = data.get('cantidad')
    id_org = data.get('id_org')

    if not nombre or not apellido_m or not apellido_p or not correo or not nacionalidad or not cantidad or not id_org:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if Donations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya está registrado"}), 400

    donacion = Donations(
        nombre=nombre,
        apellido_m=apellido_m,
        apellido_p=apellido_p,
        correo=correo,
        nacionalidad=nacionalidad,
        cantidad=cantidad,
        id_org=id_org
    )
    
    db.session.add(donacion)
    db.session.commit()

    return jsonify({
        "mensaje": "Donación creada",
        "id": donacion.id,
        "nombre": donacion.nombre,
        "apellido_m": donacion.apellido_m,
        "apellido_p": donacion.apellido_p,
        "correo": donacion.correo,
        "nacionalidad": donacion.nacionalidad,
        "cantidad": donacion.cantidad,
        "id_org": donacion.id_org
    }), 201

@jwt_required()
def obtener_donacion():
    org_id = get_jwt_identity()
    donaciones = Donations.query.filter_by(id_org=org_id).all()

    if not donaciones:
        return jsonify({"mensaje": "No se encontraron donaciones"}), 404

    return jsonify([{
        "id": donacion.id,
        "nombre": donacion.nombre,
        "apellido_m": donacion.apellido_m,
        "apellido_p": donacion.apellido_p,
        "correo": donacion.correo,
        "nacionalidad": donacion.nacionalidad,
        "cantidad": donacion.cantidad,
        "id_org": donacion.id_org
    } for donacion in donaciones]), 200