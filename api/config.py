from dotenv import load_dotenv, find_dotenv, dotenv_values
from dataclasses import dataclass


@dataclass
class Config:
    DEBUG: bool
    SECRET_KEY: str
    BCRYPT_LOG_ROUNDS: int
    TOKEN_EXPIRATION_DAYS: int
    TOKEN_EXPIRATION_SECONDS: int
    SQLALCHEMY_DATABASE_URI: str

    def get_config():
        if load_dotenv(find_dotenv(".env")) is False:
            raise Exception("Не найден файл .env")
        return Config(**dotenv_values(find_dotenv()))
