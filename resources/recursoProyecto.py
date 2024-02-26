from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.receta import Receta#ELIMINAR
from models.proyecto import Proyecto
from extensiones import db
#import json OPCION PARA TENER TILDES

#PARTE A MODIFICAR
class ProyectoListResource(Resource):
	#DEVUELVE LISTA DE PROYECTOS
    def get(self):
        datos = []
        proyectos_list = Proyecto.query.all()
        for proyecto in proyectos_list:
            datos.append(proyecto.data)
        return datos, HTTPStatus.OK

    #CREA UN NUEVO PROYECTO
    def post(self):
        datos = request.get_json()
        titulo_proyecto = datos.get('titulo')
        if Proyecto.get_by_titulo(titulo_proyecto):
            return {'message': 'Ya existe un proyecto con ese nombre.'}, HTTPStatus.BAD_REQUEST

        proyecto = Proyecto(
        	#id se genera automáticamente
            administrador=datos.get('administrador'),
            moneda=datos.get('moneda'),
            total_gastos=datos.get('total_gastos'),
            titulo=titulo_proyecto,
            descripcion=datos.get('descripcion')
        )

        proyecto.guardar()
        return proyecto.data, HTTPStatus.CREATED

class ProyectoResource(Resource):
	#DEVUELVE UN PROYECTO
    def get(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrada'}, HTTPStatus.NOT_FOUND
        return proyecto.data, HTTPStatus.OK

    #ACTUALIZA EL PROYECTO
    def put(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrada'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        proyecto.administrador = datos.get('administrador')
        proyecto.moneda = datos.get('moneda')
        proyecto.total_gastos = datos.get('total_gastos')
        proyecto.titulo = datos.get('titulo')
        proyecto.descripcion = datos.get('descripcion')
        proyecto.guardar()
        #AL ACABAR DEVUELVO EL PROYECTO/QUIZAS NO TENGA QUE HACERLO
        return proyecto.data, HTTPStatus.OK
    
    def delete(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
            return {'message': 'Proyecto no encontrada'}, HTTPStatus.NOT_FOUND
        db.session.delete(proyecto)
        db.session.commit()
        #DEBERIA ELIMINAR EL PASO DE MESSAGE?????
        return {'message': 'Proyecto eliminado'}, HTTPStatus.OK
    
class ProyectoPublishResource(Resource):
	def get(self, proyecto_id):
		proyecto = Proyecto.get_by_id(proyecto_id)
		if proyecto is None:
			return {'message': 'Proyecto no encontrada'}, HTTPStatus.NOT_FOUND
		
		#DEBERIA ELIMINAR EL PASO DE MESSAGE?????
		return {'message': 'Proyecto eliminado'}, HTTPStatus.OK
   
#ELIMINAR MÁS ADELANTE
class RecetaListResource(Resource):
    def get(self):
        datos = []
        recetas_list = Receta.query.all()
        for receta in recetas_list:
            if receta.es_publicada:
                datos.append(receta.data)
        return {'data': datos}, HTTPStatus.OK

    def post(self):
        datos = request.get_json()
        nombre_receta = datos.get('nombre')
        if Receta.get_by_nombre(nombre_receta):
            return {'message': 'Ya existe una receta con ese nombre.'}, HTTPStatus.BAD_REQUEST

        receta = Receta(
            nombre=nombre_receta,
            descripcion=datos.get('descripcion'),
            raciones=datos.get('raciones'),
            tiempo=datos.get('tiempo'),
            pasos=datos.get('pasos')
        )
        receta.guardar()
        return receta.data, HTTPStatus.CREATED

class RecetaResource(Resource):
    def get(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'Receta no encontrada'}, HTTPStatus.NOT_FOUND
        return {'data': receta.data}, HTTPStatus.OK

    def put(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'Receta no encontrada'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        receta.nombre = datos.get('nombre')
        receta.descripcion = datos.get('descripcion')
        receta.raciones = datos.get('raciones')
        receta.pasos = datos.get('pasos')
        receta.es_publicada = datos.get('es_publicada')
        receta.guardar()
        return receta.data, HTTPStatus.OK

class RecetaPublishResource(Resource):
    def put(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'Receta no encontrada'}, HTTPStatus.NOT_FOUND

        receta.es_publicada = True
        receta.guardar()
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, receta_id):
        receta = Receta.get_by_id(receta_id)
        if receta is None:
            return {'message': 'Receta no encontrada'}, HTTPStatus.NOT_FOUND

        receta.es_publicada = False
        receta.guardar()
        return {}, HTTPStatus.NO_CONTENT
