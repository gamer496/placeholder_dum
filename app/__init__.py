from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate

import cloudinary

app = Flask(__name__)
manager = Manager(app)
CORS(app)
app.config.from_object("config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

cloudinary.config(
    cloud_name = "dmi9diy4w",
    api_key = "591912672165382",
    api_secret = "rNBuN9hA1gXmlgKfsnJnZsr6JxI"
)

import models, views
