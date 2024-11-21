from flask import jsonify
from src.models.donations import Donations
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db
from src.models.membership import Membership
from src.models.donations import Donations 
import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]

@jwt_required()
def crear_donacion(data):
    nombre = data.get('nombre')
    apellido_m = data.get('apellido_m')
    apellido_p = data.get('apellido_p')
    correo = data.get('correo')
    nacionalidad = data.get('nacionalidad')
    cantidad = data.get('cantidad')
    tipo_donacion = data.get('tipo_donacion')
    id_membresia = data.get('id_membresia')
    id_org = data.get('id_org')

    if not nombre or not apellido_m or not apellido_p or not correo or not nacionalidad or not tipo_donacion or not id_org:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400

    if Donations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya está registrado"}), 400

    if tipo_donacion == 'membresia':
        membresia = Membership.query.get(id_membresia)
        if not membresia:
            return jsonify({"mensaje": "La membresía no existe"}), 404
        cantidad = membresia.costo  
    elif tipo_donacion == 'unica' and not cantidad:
        return jsonify({"mensaje": "La cantidad es obligatoria para una donación única"}), 400

    donacion = Donations(
        nombre=nombre,
        apellido_m=apellido_m,
        apellido_p=apellido_p,
        correo=correo,
        nacionalidad=nacionalidad,
        cantidad=cantidad,
        tipo_donacion=tipo_donacion,
        id_membresia=id_membresia,
        id_org=id_org
    )

    db.session.add(donacion)
    db.session.commit()


    try:
        params: resend.Emails.SendParams = {
            "from": "Organización Nutriendo A Todos <noreply@resend.dev>",
            # SOLO SE PUEDEN ENVIAR A ESTE CORREO (POR EL MOMENTO) "233358@ids.upchiapas.edu.mx"
            "to": [correo], 
            "subject": "¡Gracias por tu donación!",
            "html": f"""
            <h1>Hola {nombre} {apellido_p},</h1>
            <p>Queremos agradecerte sinceramente por tu generosa donación.</p>
            <p>Tu apoyo nos ayuda a marcar una diferencia. Estamos muy agradecidos por tu contribución de ${cantidad}.</p>
            <p>Gracias por ser parte de nuestra causa.</p>
            <br>
            <p>Atentamente,</p>
            <p>El equipo de Nutriendo A Todos</p>
            """
        }
        resend.Emails.send(params)
    except Exception as e:
        return jsonify({"mensaje": "Donación creada, pero no se pudo enviar el correo", "error": str(e)}), 500

    return jsonify({
        "mensaje": "Donación creada y correo enviado",
        "id": donacion.id,
        "nombre": donacion.nombre,
        "apellido_m": donacion.apellido_m,
        "apellido_p": donacion.apellido_p,
        "correo": donacion.correo,
        "nacionalidad": donacion.nacionalidad,
        "cantidad": donacion.cantidad,
        "tipo_donacion": donacion.tipo_donacion,
        "id_org": donacion.id_org
    }), 201


@jwt_required()
def obtener_donacion():
    org_id = get_jwt_identity()
    donaciones = Donations.query.filter_by(id_org=org_id).all()

    if not donaciones:
        return jsonify({"mensaje": "No se encontraron donaciones"}), 404

    return jsonify({
        "id": donaciones.id,
        "nombre": donaciones.nombre,
        "apellido_m": donaciones.apellido_m,
        "apellido_p": donaciones.apellido_p,
        "correo": donaciones.correo,
        "nacionalidad": donaciones.nacionalidad,
        "cantidad": donaciones.cantidad,
        "id_org": donaciones.id_org
    }), 200

@jwt_required()
def obtener_donacionesByID_org(org_id):
    donaciones = Donations.query.filter_by(id_org=org_id).all()

    if not donaciones:
        return jsonify({"mensaje": "No se encontraron donaciones para esta organización"}), 404

    return jsonify([{
        "id": donacion.id,
        "nombre": donacion.nombre,
        "apellido_m": donacion.apellido_m,
        "apellido_p": donacion.apellido_p,
        "correo": donacion.correo,
        "nacionalidad": donacion.nacionalidad,
        "cantidad": donacion.cantidad,
        "tipo_donacion": donacion.tipo_donacion,
        "id_org": donacion.id_org
    } for donacion in donaciones]), 200