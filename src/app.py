"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


# create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET', 'POST'])
def members():
    response_body = {}
    if request.method == 'GET':
        members = jackson_family.get_all_members()
        response_body['message'] = 'Listado de los integrantes de la familia'
        response_body['results'] = members
        return response_body, 200
    if request.method == 'POST':
        new_member = request.json
        jackson_family.add_member(new_member)
        response_body['message'] = 'Respuesta desde el POST de members'
        response_body['results'] = jackson_family.get_all_members()
        return response_body, 200


@app.route('/members/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def member(id):
    response_body = {}
    if not jackson_family.get_member(id):
        response_body['message'] = f'No existe el usuario {id}'
        response_body['results'] = []
        return response_body, 400
    if request.method == 'GET':
        response_body['message'] = f'Member con id {id}'
        response_body['results'] = jackson_family.get_member(id)
        return response_body, 200
    if request.method == 'PUT':
        member_to_update = request.json
        keys = member_to_update.keys()
        if 'name' not in keys or 'age' not in keys or 'lucky_numbers' not in keys:
            response_body['message'] = 'Datos incorrectos'
            response_body['results'] = []
            return response_body, 400
        jackson_family.update_member(member_to_update, id)
        response_body['message'] = f'Member con id {id} actualizado correctamente'
        response_body['results'] = jackson_family.get_all_members()
        return response_body, 200
    if request.method == 'DELETE':
        jackson_family.delete_member(id)
        response_body['message'] = f'Member con id {id} eliminado correctamente'
        response_body['results'] = jackson_family.get_all_members()
        return response_body, 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
