from datetime import timedelta

class Config:
    # Base de datos
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:TavoHueco123@34.58.54.99/imporcomgua"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT
    SECRET_KEY = 'dev-secret-key-change-in-production'
    JWT_SECRET_KEY = SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'

    # Email
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = '587'
    EMAIL_USER = 'panfilo.pf.pf88@gmail.com'
    EMAIL_PASSWORD = 'naqb pyby rejc hrnh'
    
    # Alerta
    STOCK_MINIMO_ALERTA = '100'

    # Otros
    ENV = 'production'
    DEBUG = False


# import os
# from dotenv import load_dotenv
# from datetime import timedelta

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, '..', '.env'))

# class Config:
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{os.getenv('root')}:{os.getenv('TavoHueco123')}"
#         f"@{os.getenv('34.58.54.99')}/{os.getenv('imporcomgua')}"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
#     SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
#     JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
#     JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
#     JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
#     JWT_ALGORITHM = 'HS256'

#     EMAIL_HOST='smtp.gmail.com'
#     EMAIL_PORT='587'
#     EMAIL_USER='panfilo.pf.pf88@gmail.com'
#     EMAIL_PASSWORD='naqb pyby rejc hrnh'
#     STOCK_MINIMO_ALERTA='100'