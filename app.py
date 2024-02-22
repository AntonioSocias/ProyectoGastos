from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensiones import db
from models.receta import Receta#eliminar
from models.proyecto import Proyecto
from resources.recursosReceta import RecetaListResource, RecetaResource, RecetaPublishResource, ProyectoListResource, ProyectoResource, ProyectoPublishResource

import subprocess
import time

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resource(app)
    return app

def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)

def register_resource(app):
    api = Api(app)
    api.add_resource(ProyectoListResource, '/projects')
    api.add_resource(ProyectoResource, '/projects/<int:proyecto_id>')#REVISAR ESTO MÁS TARDE
    api.add_resource(RecetaListResource, '/smilecook')#eliminar
    api.add_resource(RecetaResource, '/smilecook/<int:receta_id>')#eliminar
    api.add_resource(RecetaPublishResource, '/smilecook/<int:receta_id>/publish')#eliminar

app = create_app()
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Receta=Receta)
    
def git_pull():
    subprocess.run(["git", "pull"])

if __name__ == "__main__":
    while True:
        git_pull()
        time.sleep(10)