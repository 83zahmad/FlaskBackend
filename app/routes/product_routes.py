from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.product_service import (
    get_all_products,
    get_product_by_id,
    create_product,
    update_product,
    delete_product
)
from app.models.user_model import User

product_bp = Blueprint('product', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    products = get_all_products()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(product.to_dict()), 200

@product_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')
    stock = data.get('stock')

    if not all([name, price, stock]):
        return jsonify({'error': 'Missing required fields'}), 400

    product, error = create_product(name, description, price, image_url, stock)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Product created successfully', 'product': product.to_dict()}), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def edit_product(product_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    product, error = update_product(product_id, **data)
    
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_product(product_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user or not user.is_admin:
        return jsonify({'error': 'Admin access required'}), 403

    result, error = delete_product(product_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify({'message': 'Product deleted successfully'}), 200 