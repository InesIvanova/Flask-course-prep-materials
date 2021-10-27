from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api

from db import db
from resources.routes import routes

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

api = Api(app)
migrate = Migrate(app, db)
CORS(app)


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.after_request
def close_request(response):
    db.session.commit()
    return response


[api.add_resource(*route) for route in routes]


if __name__ == '__main__':
    app.run()