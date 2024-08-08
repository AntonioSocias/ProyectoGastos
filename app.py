from flask import Flask, render_template
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensiones import db


#IMPORTACIÓN DE RECURSOS
from resources.recursoProyecto import ProyectoListResource, ProyectoResource, ProyectoGastos, ProyectoUsuarios 
from resources.recursoGasto import GastoListResource, GastoResource
from resources.recursoProyectoUsuario import ProyectosUsuariosListResource, ProyectoUsuariosListResource
from resources.recursoUsuario import UsuarioListResource, UsuarioResource
from resources.recursoParte import ParteListResource, ParteResource 


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
    api.add_resource(ProyectoListResource, '/proyectos')#GET - devuelve una lista de proyectos POST - crea un nuevo proyecto
    api.add_resource(ProyectoResource, '/proyectos/<int:proyecto_id>')#actualiza y elimina un proyecto 
    api.add_resource(ProyectoGastos, '/proyectos/<int:proyecto_id>/gastos')#devuelve lista de gastos del proyecto
    api.add_resource(ProyectoUsuarios, '/proyectos/<int:proyecto_id>/usuarios')#devuelve lista de usuarios del proyecto 

    api.add_resource(GastoListResource, '/gastos')##GET - devuelve una lista de gastos POST - crea un nuevo gasto
    api.add_resource(GastoResource, '/gastos/<int:gasto_id>')#actualiza o elimina un gasto
    
    api.add_resource(UsuarioListResource, '/usuarios')#devuelve una lista de usuarios
    api.add_resource(UsuarioResource, '/usuarios/<int:usuario_id>')#actualiza o elimina un usuario
    
    api.add_resource(ParteListResource, '/partes')#devuelve una lista de partes
    api.add_resource(ParteResource, '/partes/<int:parte_id>')#actualiza o elimina un parte
    
    api.add_resource(ProyectosUsuariosListResource, '/relacion')##GET - devuelve una lista de relaciones Proyectos_usuarios POST - crea una nueva relación
    api.add_resource(ProyectoUsuariosListResource, '/relacion/<int:proyecto_id>')#actualiza o elimina una relación de proyectos y usuarios

def register_routes(app):
    @app.route('/')
    def index():
        return render_template('marina.html')

app = create_app()

#REVISAR QUE HACE ESTO 
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Receta=Receta)