from app import db
from app.models.user_model import User
from flask_jwt_extended import create_access_token

def register_user(username, email, password, first_name, last_name):
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return None, "Email already registered"
    if User.query.filter_by(username=username).first():
        return None, "Username already taken"

    # Create new user
    user = User(
        username=username,
        email=email,
        first_name=first_name,
        last_name=last_name
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, str(e)

def login_user(email, password):
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return None, "Invalid email or password"
    
    # Create access token
    access_token = create_access_token(identity=user.id, additional_claims={"is_admin": user.is_admin})
    return {"access_token": access_token, "user": user.to_dict()}, None 