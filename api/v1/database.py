from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, timedelta
from api import db, bcrypt
from uuid import uuid4
from flask import current_app
import jwt


class User(db.Model):
    __tablename__ = "users"
    user_uuid: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    last_active: Mapped[datetime] = mapped_column(DateTime, nullable=True, default=None)

    def __init__(self, name: str, username: str, email: str, password: str):
        self.user_uuid = str(uuid4())
        self.name = name
        self.username = username
        self.email = email
        self.created_at = datetime.utcnow()
        self.last_active = datetime.utcnow()

        pwd = bcrypt.generate_password_hash(password.encode("utf-8"), rounds=int(current_app.config.get("BCRYPT_LOG_ROUNDS")))
        self.password = pwd.decode("utf-8")

    def to_dict(self) -> dict:
        return {
            "uuid": self.user_uuid,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "created_at": self.created_at,
            "last_active": self.last_active,
        }
    
    def generate_auth_token(self):
        try:
            payload = {
                "exp": datetime.utcnow() + timedelta(
                    days=float(current_app.config.get("TOKEN_EXPIRATION_DAYS")),
                    seconds=float(current_app.config.get("TOKEN_EXPIRATION_SECONDS")),
                ),
                "iat": datetime.utcnow(),
                "sub": self.user_uuid,
            }
            token = jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
            return token
        except Exception as e:
            raise e
    
    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                current_app.config.get("SECRET_KEY"),
                algorithms=["HS256"]
            )
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Токен авторизации устарел. Пожалуйста, войдите в систему повторно."
        except jwt.InvalidTokenError as e:
            return e
            return "Неверный токен авторизации. Пожалуйста, войдите в систему повторно."


class UserAndCards(db.Model):
    __tablename__ = "user_and_cards"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_uuid: Mapped[int] = mapped_column(String, nullable=False)
    card_uuid: Mapped[int] = mapped_column(String, nullable=False, unique=True)

    def __init__(self, user_uuid, card_uuid):
        self.user_uuid = user_uuid
        self.card_uuid = card_uuid


class Card(db.Model):
    __tablename__ = "cards"
    card_uuid: Mapped[str] = mapped_column(String, primary_key=True)
    header: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    links: Mapped[str] = mapped_column(String, nullable=True)
    picture_path: Mapped[str] = mapped_column(String, nullable=True)
    emoji: Mapped[str] = mapped_column(String, nullable=True)

    def __init__(self, header, content, links = None, emoji = None):
        self.card_uuid == str(uuid4)
        self.header = header
        self.content = content
        self.links = links
        self.emoji = emoji

    def to_dict(self) -> dict:
        return {
            "uuid": self.card_uuid,
            "header": self.header,
            "content": self.content,
            "links": self.links,
            "picture_path": self.picture_path,
            "emoji": self.emoji,
        }