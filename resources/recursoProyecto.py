from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.gasto import Gasto
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
    #OBTENER GASTOS DEL PROYECTO PASADO
    def get(self, proyecto_id):
        proyecto = Proyecto.get_by_id(proyecto_id)
        if proyecto is None:
             return {'message': 'Proyecto no encontrada'}, HTTPStatus.NOT_FOUND
        lista_gastos = Gasto.query.all()
        lista_gastos_proyecto = []
        for gasto in lista_gastos:
          if gasto.proyecto == proyecto_id:  
            lista_gastos_proyecto.append(gasto)
		return {'message': 'Lista de gastos devuelta'}, HTTPStatus.OK