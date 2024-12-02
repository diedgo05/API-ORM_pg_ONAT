from flask import jsonify, request
from src.models.organizations import Organizations
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from src.models import db
from google.cloud import storage



def upload_to_cloud_storage(file, bucket_name, destination_blob_name):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_file(file, content_type=file.content_type)
    return blob.public_url

# Modificación en crear una organización para permitir consultas en postman o thunderclient con form-data
def crear_org():
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    cp = request.form.get('cp')
    estado = request.form.get('estado')
    direccion = request.form.get('direccion')
    rfc = request.form.get('rfc')

    telefono = request.form.get('telefono')
    contrasena = request.form.get('contrasena')
    imagen = request.files.get('imagen')
    municipio = request.form.get('municipio')
    colonia = request.form.get('colonia')

    
    if not nombre or not correo or not estado or not rfc or not telefono or not contrasena:
        return jsonify({"mensaje": "Faltan campos obligatorios" }), 400
    
    if Organizations.query.filter_by(correo=correo).first():
        return jsonify({"mensaje": "El correo ya esta registrado"}), 400
    
    if imagen: 
        imagen_url = upload_to_cloud_storage(imagen, "nombre-del-bucket", f"organizaciones/{imagen.filename}")
    else:
        return jsonify({"mensaje": "Falta la imagen"}), 400
    
    nueva_org = Organizations(nombre=nombre, 
    correo=correo,
    estado=estado,
     cp=cp,
    municipio=municipio, 
    colonia=colonia,
    rfc=rfc,
    telefono=telefono,
    contrasena=contrasena,
    direccion=direccion,
    imagen=imagen_url
    ) 


    db.session.add(nueva_org)
    db.session.commit()

    return jsonify({"mensaje": "Organización creada", "id": nueva_org.id, "correo": nueva_org.correo}), 201

def login_organizacion(data):
    correo = data.get('correo')
    contraseña = data.get('contrasena')
    
    if not correo or not contraseña:
        return jsonify({"mensaje": "Faltan campos obligatorios"}), 400
    
    organizacion = Organizations.query.filter_by(correo=correo).first()

    if not organizacion:
        return jsonify({"mensaje": "Credenciales inválidas"}), 401
    if not organizacion.check_contraseña(contraseña):
        return jsonify({"mensaje": "Credenciales inválidas"}), 401

    # access_token = create_access_token(identity=organizacion.id,)
    access_token = create_access_token(identity=str(organizacion.id))  # Convertir a string
    return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200


def obtener_organizaciones():
    # organizacion_id = get_jwt_identity()
    organizaciones = Organizations.query.all()
    lista_organizaciones = []
    for org in organizaciones:
        lista_organizaciones.append({
            "id": org.id,
            "nombre": org.nombre,
            "correo": org.correo,
            "cp": org.cp,
            "estado": org.estado,
            "direccion": org.direccion,
            "rfc": org.rfc,
            "telefono": org.telefono
        })

    if not organizaciones:
        return jsonify({"mensaje": "Organizaciones no encontradas"}), 404
    return jsonify(lista_organizaciones), 200

def obtener_organizacion_por_id(id):
    # Buscar la organización por id
    organizacion = Organizations.query.get(id)
    
    if not organizacion:
        return jsonify({"mensaje": "Organización no encontrada"}), 404
    
    # Retornar los datos de la organización en formato JSON
    return jsonify({
        "id": organizacion.id,
        "nombre": organizacion.nombre,
        "correo": organizacion.correo,
        "cp": organizacion.cp,
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

#@jwt_required()  # Protege esta ruta, requiere un token válido
def validarToken():
    try:
        verify_jwt_in_request();
        # Si el token es válido, esta línea se ejecutará
        user_identity = get_jwt_identity()  # Obtiene la información del token (por ejemplo, el ID del usuario)
        print(get_jwt_identity())
        # Respuesta con los datos del token
        return jsonify({ 
        }), 200

    except Exception as e:
        # En caso de que el token no sea válido o falten permisos
        return jsonify({
            "mensaje": "Token inválido o no proporcionado",
            "error": str(e)
        }), 401
    

