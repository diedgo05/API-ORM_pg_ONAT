from flask import jsonify, request
from src.models.organizations import Organizations, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# Modificación en crear una organización para permitir consultas en postman o thunderclient con form-data
def crear_org():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    estado = request.form.get('estado')
    direccion = request.form.get('direccion')
    rfc = request.form.get('rfc')
    telefono = request.form.get('telefono')
    contraseña = request.form.get('contraseña')
    imagen = request.files.get('imagen')

    if not nombre or not correo or not estado or not rfc or not telefono or not contraseña:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
    
    if Organizations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya esta registrado"}), 400
    
    if imagen:
        imagen_data = imagen.read()
    else:
        return jsonify({"mensaje": "Falta la imagen"}), 400
    
    nueva_org = Organizations(nombre=nombre, correo=correo, estado=estado, rfc=rfc, telefono=telefono, contraseña=contraseña, direccion=direccion, imagen=imagen_data) 
    db.session.add(nueva_org)
    db.session.commit()

    return jsonify({"mensaje": "Organización creada", "id": nueva_org.id, "correo": nueva_org.correo}), 201

def login_organizacion(data):
    correo = data.get('correo')
    contraseña = data.get('contraseña')
    
    if not correo or not contraseña:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
    
    organizacion = Organizations.query.filter_by(correo=correo).first()

    if not organizacion:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    if not organizacion.check_contraseña(contraseña):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=organizacion.id)
    return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200

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
        "estado": organizacion.estado,
        "direccion": organizacion.direccion,
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