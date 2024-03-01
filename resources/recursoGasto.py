from datetime import datetime
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.gasto import Gasto
from extensiones import db
#import json OPCION PARA TENER TILDES

#PARTE A MODIFICAR
class GastoListResource(Resource):
	#DEVUELVE LISTA DE GASTOS
    def get(self):
        datos = []
        gastos_list = Gasto.query.all()
        for gasto in gastos_list:
            datos.append(gasto.data)
        return datos, HTTPStatus.OK

    #CREA UN NUEVO GASTO
    def post(self):
        datos = request.get_json()
        titulo_gasto = datos.get('titulo')
        if Gasto.get_by_titulo(titulo_gasto):
            return {'message': 'Ya existe un gasto con ese nombre.'}, HTTPStatus.BAD_REQUEST
        print(datos.get('fecha'))

        fechaAdaptada = datos.get('fecha').date()

        gasto = Gasto(
        	#id se genera automáticamente
            fecha=fechaAdaptada,
            pagador=datos.get('pagador'),
            cantidad=datos.get('cantidad'),
            proyecto = datos.get('proyecto'),
            titulo=titulo_gasto
        )

        gasto.guardar()
        return gasto.data, HTTPStatus.CREATED

class GastoResource(Resource):
	#DEVUELVE UN GASTO
    def get(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrada'}, HTTPStatus.NOT_FOUND
        return gasto.data, HTTPStatus.OK

    #ACTUALIZA EL GASTO
    def put(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrada'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        gasto.titulo = datos.get('titulo')
        gasto.pagador = datos.get('pagador')
        gasto.cantidad = datos.get('cantidad')
        gasto.fecha = datos.get('fecha')
        gasto.proyecto = datos.get('proyecto')
        gasto.guardar()
        #AL ACABAR DEVUELVO EL GASTO/QUIZAS NO TENGA QUE HACERLO
        return gasto.data, HTTPStatus.OK
    #ELIMINA EL GASTO
    def delete(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrada'}, HTTPStatus.NOT_FOUND
        db.session.delete(gasto)
        db.session.commit()
		#DEBERIA ELIMINAR EL PASO DE MESSAGE?????
        return {'message': 'Gasto eliminado'}, HTTPStatus.OK