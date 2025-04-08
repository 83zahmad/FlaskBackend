from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not all([username, email, password, first_name, last_name]):
        return jsonify({'error': 'Missing required fields'}), 400

    user, error = register_user(username, email, password, first_name, last_name)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'User registered successfully', 'user': user.to_dict()}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({'error': 'Missing email or password'}), 400

    result, error = login_user(email, password)
    if error:
        return jsonify({'error': error}), 401

    return jsonify(result), 200 