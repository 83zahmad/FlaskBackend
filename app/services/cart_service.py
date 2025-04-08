from app import db
from app.models.cart_model import Cart, CartItem
from app.models.product_model import Product

def get_or_create_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()
    return cart

def add_to_cart(user_id, product_id, quantity=1):
    cart = get_or_create_cart(user_id)
    product = Product.query.get(product_id)
    
    if not product:
        return None, "Product not found"
    
    if product.stock < quantity:
        return None, "Insufficient stock"
    
    # Check if product already in cart
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
    
    try:
        db.session.commit()
        return cart.to_dict(), None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def remove_from_cart(user_id, product_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return None, "Cart not found"
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        return None, "Product not in cart"
    
    try:
        db.session.delete(cart_item)
        db.session.commit()
        return cart.to_dict(), None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def update_cart_item_quantity(user_id, product_id, quantity):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return None, "Cart not found"
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
    if not cart_item:
        return None, "Product not in cart"
    
    product = Product.query.get(product_id)
    if product.stock < quantity:
        return None, "Insufficient stock"
    
    cart_item.quantity = quantity
    
    try:
        db.session.commit()
        return cart.to_dict(), None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def clear_cart(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return None, "Cart not found"
    
    try:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        return cart.to_dict(), None
    except Exception as e:
        db.session.rollback()
        return None, str(e) 