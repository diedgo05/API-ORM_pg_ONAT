from flask import jsonify
from src.models.membership import Membership
from src.models import db


def crear_membresia(data):
    plan = data.get('plan')
    costo = data.get('costo')
    contenido = data.get('contenido')

    if not plan or not costo or not contenido: 
        return jsonify({"mensaje":"Faltan campos obligatorios a rellenar"}),400 
    
    nueva_membresia = Membership(
        plan=plan,
        costo=costo,
        contenido=contenido
    )

    db.session.add(nueva_membresia)
    db.session.commit()

    return jsonify({
        "mensaje":"Membresía creada correctamente",
        "id": nueva_membresia.id,
        "plan": nueva_membresia.plan,
        "costo":nueva_membresia.costo,
        "contenido":nueva_membresia.checar_contenido()
    }), 201

def obtener_membresias():
    memberships = Membership.query.all()
    
    if not memberships:
        return jsonify({"mensaje": "Membresías no encontrado"}), 404
    

    return jsonify([{
        "id": membership.id,
        "plan": membership.plan,
        "costo": membership.costo ,
        "contenido": membership.checar_contenido()
    }for membership in memberships]), 200

def obtener_membresia_byID(id):
    membresia = Membership.query.get(id)
    
    if not membresia:
        return jsonify({"mensaje": "Membresía no encontrada"}), 404

    return jsonify({
        "id": membresia.id,
        "plan": membresia.plan,
        "costo": membresia.costo,
        "contenido": membresia.checar_contenido()
    }), 200
