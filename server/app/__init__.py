import os
from flask import Flask,request
import app.config as config
from app.Controllers import userController
from app.models import db

app = Flask(__name__)

if os.environ.get("APP_ENV") == "dev":
    app.config.from_object(config.DevelopmentConfig)
elif os.environ.get("APP_ENV") == "prod":
    app.config.from_object(config.ProductionConfig)

db.__init__(app)

app.register_blueprint(userController.bp)

if __name__ ==  "__main__":
    app.run(debug=True)