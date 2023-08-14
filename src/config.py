from dotenv import dotenv_values
from datetime import timedelta

class Config:
    JWT_SECRET_KEY=dotenv_values('.env').get('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(seconds=10)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(hours=1)

    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_USERNAME = dotenv_values('.env').get('MAIL_USERNAME')
    MAIL_PASSWORD = dotenv_values('.env').get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = dotenv_values('.env').get('MAIL_USERNAME')


class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI=dotenv_values('.env').get('DATABASE_URL')

config = {
    'development': DevelopmentConfig
}