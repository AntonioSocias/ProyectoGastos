from flask import Flask
from flask_restful import Api
from config import Config
from extensiones import db
from models.receta import Receta
from resources.recursosReceta import RecetaListResource, RecetaResource, RecetaPublishResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resource(app)
    return app

def register_extensions(app):
    db.init_app(app)

def register_resource(app):
    api = Api(app)
    api.add_resource(RecetaListResource, '/smilecook')
    api.add_resource(RecetaResource, '/smilecook/<int:receta_id>')
    api.add_resource(RecetaPublishResource, '/smilecook/<int:receta_id>/publish')

app = create_app()
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Receta=Receta)
