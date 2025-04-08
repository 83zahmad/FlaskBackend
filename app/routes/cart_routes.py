from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.cart_service import (
    get_or_create_cart,
    add_to_cart,
    remove_from_cart,
    update_cart_item_quantity,
    clear_cart
)

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    current_user_id = get_jwt_identity()
    cart = get_or_create_cart(current_user_id)
    return jsonify(cart.to_dict()), 200

@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_item():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    cart, error = add_to_cart(current_user_id, product_id, quantity)
    if error:
        return jsonify({'error': error}), 400

    return jsonify(cart), 200

@cart_bp.route('/remove', methods=['POST'])
@jwt_required()
def remove_item():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    cart, error = remove_from_cart(current_user_id, product_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify(cart), 200

@cart_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_item():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not all([product_id, quantity]):
        return jsonify({'error': 'Product ID and quantity are required'}), 400

    cart, error = update_cart_item_quantity(current_user_id, product_id, quantity)
    if error:
        return jsonify({'error': error}), 400

    return jsonify(cart), 200

@cart_bp.route('/clear', methods=['POST'])
@jwt_required()
def clear():
    current_user_id = get_jwt_identity()
    cart, error = clear_cart(current_user_id)
    if error:
        return jsonify({'error': error}), 400

    return jsonify(cart), 200

# TODO: Implement Stripe payment integration
# @cart_bp.route('/checkout', methods=['POST'])
# @jwt_required()
# def checkout():
#     current_user_id = get_jwt_identity()
#     cart = get_or_create_cart(current_user_id)
#     
#     # TODO: Implement Stripe payment processing
#     # 1. Create Stripe payment intent
#     # 2. Process payment
#     # 3. Update inventory
#     # 4. Clear cart
#     # 5. Return success response
#     
#     return jsonify({'error': 'Payment processing not implemented'}), 501 