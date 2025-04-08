from app import db
from app.models.product_model import Product

def get_all_products():
    return Product.query.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def create_product(name, description, price, image_url, stock):
    product = Product(
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        stock=stock
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        return product, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def update_product(product_id, **kwargs):
    product = Product.query.get(product_id)
    if not product:
        return None, "Product not found"
    
    for key, value in kwargs.items():
        if hasattr(product, key):
            setattr(product, key, value)
    
    try:
        db.session.commit()
        return product, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return None, "Product not found"
    
    try:
        db.session.delete(product)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return None, str(e) 