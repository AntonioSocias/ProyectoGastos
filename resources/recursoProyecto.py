from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.modelosGeneral import Gasto, Usuario, Proyecto
from extensiones import db

class ProyectoListResource(Resource):
    # DEVUELVE LISTA DE PROYECTOS
    def get(self):
        proyectos = Proyecto.query.all()
        datos = [proyecto.data for proyecto in proyectos]
        return datos, HTTPStatus.OK

    # CREA UN NUEVO PROYECTO
    def post(self):
        datos = request.get_json()
        titulo_proyecto = datos.get('titulo')
        
        # Verificar si ya existe un proyecto con el mismo título
        if Proyecto.get_by_titulo(titulo_proyecto):
            return {'message': 'Ya existe un proyecto con ese nombre.'}, HTTPStatus.BAD_REQUEST

        proyecto = Proyecto(
            administrador=datos.get('administrador_id'),
            moneda=datos.get('moneda_id'),
            titulo=titulo_proyecto,
            descripcion=datos.get('descripcion')
        )

        proyecto.guardar()
        return proyecto.data, HTTPStatus.CREATED

class ProyectoResource(Resource):
    # DEVUELVE UN PROYECTO
    def get(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrado'}, HTTPStatus.NOT_FOUND
        return proyecto.data, HTTPStatus.OK

    # ACTUALIZA EL PROYECTO
    def put(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrado'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        proyecto.administrador = datos.get('administrador_id')
        proyecto.moneda = datos.get('moneda_id')
        proyecto.titulo = datos.get('titulo')
        proyecto.descripcion = datos.get('descripcion')
        proyecto.guardar()
        return proyecto.data, HTTPStatus.OK
    
    # ELIMINA EL PROYECTO
    def delete(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrado'}, HTTPStatus.NOT_FOUND
        
        # Eliminar todos los gastos asociados al proyecto
        lista_gastos_proyecto = Gasto.query.filter_by(proyecto_id=proyecto_id).all()
        for gasto in lista_gastos_proyecto:
            db.session.delete(gasto)
        
        # Eliminar el proyecto
        db.session.delete(proyecto)
        db.session.commit()
        return {'message': 'Proyecto eliminado'}, HTTPStatus.OK

class ProyectoGastos(Resource):
    # OBTENER GASTOS DEL PROYECTO
    def get(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrado'}, HTTPStatus.NOT_FOUND
        
        # Obtener todos los gastos asociados al proyecto
        lista_gastos = Gasto.query.filter_by(proyecto_id=proyecto_id).all()
        datos = [gasto.data for gasto in lista_gastos]
        return datos, HTTPStatus.OK

class ProyectoUsuarios(Resource):
    # OBTENER USUARIOS DEL PROYECTO
    def get(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrado'}, HTTPStatus.NOT_FOUND
        
        # Obtener todos los usuarios asociados al proyecto
        lista_usuarios = Usuario.query.filter_by(proyecto_id=proyecto_id).all()
        datos = [usuario.data for usuario in lista_usuarios]
        return datos, HTTPStatus.OK
