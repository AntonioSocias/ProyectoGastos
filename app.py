from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensiones import db

#IMPORTACIÓN DE MODELOS
from models.proyecto import Proyecto
from models.gasto import Gasto
from models.receta import Receta
#IMPORTACIÓN DE RECURSOS
from resources.recursoProyecto import ProyectoListResource, ProyectoResource, ProyectoPublishResource
from resources.recursoGasto import GastoListResource, GastoResource


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
    api.add_resource(ProyectoListResource, '/proyectos')#devuelve una lista de proyectos
    api.add_resource(ProyectoResource, '/proyectos/<int:proyecto_id>')#crea y elimina un proyecto 
    api.add_resource(ProyectoPublishResource, '/proyectos/<int:proyecto_id>/gastos')#devuelve lista de gastos del proyecto 
    api.add_resource(GastoListResource, '/gastos')#devuelve una lista de gastos
    api.add_resource(GastoResource, '/gastos/<int:gasto_id>')#crea un gasto
app = create_app()

#REVISAR QUE HACE ESTO 
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Receta=Receta)