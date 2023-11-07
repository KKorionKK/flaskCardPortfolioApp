from flask_sqlalchemy import SQLAlchemy
from api.v1.database import User
from sqlalchemy import select
from api import bcrypt
from flask import make_response, Response, request, session, redirect

def get_user_by_email(email: str, db: SQLAlchemy) -> User | None:
    return db.session.scalar(
        select(
            User
        )
        .where(User.email == email)
    )

def user_login(user_data: dict[str, str], db: SQLAlchemy) -> tuple | Response:
    user: User | None = get_user_by_email(user_data.get("email"), db=db)
    if not user:
        return ("Пользователь с таким email не найден", 400)
    else:
        if bcrypt.check_password_hash(user.password, user_data.get("password")):
            auth_token = user.generate_auth_token()
            if auth_token:
                response = make_response()
                response.status = 200
                response.set_cookie("auth_token", auth_token)
                return response
        else:
            return ("Неверные данные", 400)

def user_register(user_data: dict[str, str], db: SQLAlchemy) -> tuple | Response:
    user: User | None = get_user_by_email(user_data.get("email"), db=db)
    if user:
        return ("Пользователь с таким email уже существует", 400)
    else:
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        auth_token = new_user.generate_auth_token()
        if auth_token:
            response = make_response()
            response.status = 200
            response.set_cookie("auth_token", auth_token)
            return response
    return ("Пользователь успешно создан", 200)



def authorization_required(endpoint):
    def decorated_function(*args, **kwargs):
        auth_token: str = request.cookies.get("auth_token")
        auth_error = ("Для продолжения требуется авторизация", 401)
        if not auth_token:
            return auth_error
        response = User.decode_auth_token(auth_token=auth_token)
        user = User.query.filter_by(user_uuid=response).first()
        if not user:
            return auth_error
        return endpoint(*args, **kwargs)

    return decorated_function

