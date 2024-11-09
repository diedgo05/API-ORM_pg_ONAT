import requests
from flask import jsonify, request
from src.models import db

def get_cp():
    cp = request.args.get('cp')
    key = 'ab716732e7bc9c7aab8e35ae879d397e920b1d61'

    try:
        response = requests.get(
            f'https://api.tau.com.mx/dipomex/v1/codigo_postal?cp={cp}',
            headers={'APIKEY': key}
        )

        data = response.json()

        if not data.get('error'):
            return jsonify(data)

        return jsonify({"error": "No se encontró dicho código postal"}), 404

    except Exception as err:
        return jsonify({"error": str(err)}), 500
    