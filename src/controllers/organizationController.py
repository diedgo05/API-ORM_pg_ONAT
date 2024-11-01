from flask import jsonify
from src.models.organizations import Organizations, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def crear_org(data):
    nombre = data.get('nombre')
    correo = data.get('correo')
    pais = data.get('pais')
    rfc = data.get('rfc')
    telefono = data.get('telefono')
    contraseña = data.get('contraseña')

    if not nombre or not correo or not pais or not rfc or not telefono or not contraseña:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
    
    if Organizations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya esta registrado"}), 400
    
    nueva_org = Organizations(nombre=nombre, correo=correo, pais=pais, rfc=rfc, telefono=telefono, contraseña=contraseña) 
    db.session.add(nueva_org)
    db.session.commit()

    return jsonify({"mensaje": "Organización creada", "id": nueva_org.id, "correo": nueva_org.correo}), 201

def login_organizacion(data):
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    organizacion = Organizations.query.filter_by(correo=correo).first()

    if not organizacion:
        return jsonify({"mensaje":"Credenciales invalidas"}), 401
    if not organizacion.check_contraseña(contraseña):
        access_token = create_access_token(identity=organizacion.id)
        return jsonify({"mensaje":"Inicio de sesión exitoso", "token":access_token}), 200

@jwt_required()
def obtener_organizaciones():
    organizacion_id = get_jwt_identity()
    organizacion = Organizations.query.get(organizacion_id)
    if not organizacion:
        return jsonify({"mensaje": "Organizaciones no encontradas"}), 404
    return jsonify({
        "id": organizacion.id,
        "nombre": organizacion.nombre,
        "correo": organizacion.correo,
        "pais": organizacion.pais,
        "rfc": organizacion.rfc,
        "telefono": organizacion.telefono
                  }), 200

@jwt_required()
def actualizar_organizaciones(id, data):
    org_id = get_jwt_identity()
    organizacion = Organizations.query.get(id)
    if org_id != id:
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
        "mensaje":"Datos de la organización actualizadas correctamente",
        "id":organizacion.id,
        "nombre":organizacion.nombre,
        "correo":organizacion.correo,
        "telefono":organizacion.telefono}), 200

# Voy a crear este controlador, pero no se si es necesario (eliminar)
@jwt_required()
def eliminar_organizacion(id):
    organizacion = Organizations.query.get(id)
    if not organizacion:
        return jsonify({"mensaje":"Organización benéfica no encontrada"}), 404
    db.session.delete(organizacion)
    db.session.commit()
    return jsonify({"mensaje":"Organización eliminada correctamente"}), 200