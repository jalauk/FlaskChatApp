import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())

class Config():
    MONGODB_SETTINGS = {
        'host' : os.environ.get("MONGODB_SETTINGS")
    }
    ACCESS_TOKEN_EXP_TIME=os.environ.get("ACCESS_TOKEN_EXP_TIME")
    REFRESH_TOKEN_EXP_TIME=os.environ.get("REFRESH_TOKEN_EXP_TIME")
    ACCESS_TOKEN_SECRET_KEY=os.environ.get("ACCESS_TOKEN_SECRET_KEY")
    REFRESH_TOKEN_SECRET_KEY=os.environ.get("REFRESH_TOKEN_SECRET_KEY")

class DevelopmentConfig(Config):
    DEBUG=True

class ProductionConfig(Config):
    DEBUG=False