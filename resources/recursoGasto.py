from datetime import datetime
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.gasto import Gasto
from extensiones import db

class GastoListResource(Resource):
    # DEVUELVE LISTA DE GASTOS
    def get(self):
        gastos = Gasto.query.all()
        datos = [gasto.data for gasto in gastos]
        return datos, HTTPStatus.OK

    # CREA UN NUEVO GASTO
    def post(self):
        datos = request.get_json()
        titulo_gasto = datos.get('titulo')
        
        # Adapto la fecha al formato de datetime
        fecha_str = datos.get('fecha')
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        
        gasto = Gasto(
            fecha=fecha,
            pagador_id=datos.get('pagador'),
            cantidad=datos.get('cantidad'),
            proyecto_id=datos.get('proyecto'),
            titulo=titulo_gasto
        )

        db.session.add(gasto)
        db.session.commit()
        return gasto.data, HTTPStatus.CREATED

class GastoResource(Resource):
    # DEVUELVE UN GASTO
    def get(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrado'}, HTTPStatus.NOT_FOUND
        return gasto.data, HTTPStatus.OK

    # ACTUALIZA EL GASTO
    def put(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrado'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        titulo_gasto = datos.get('titulo')
        fecha_str = datos.get('fecha')
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        gasto.titulo = titulo_gasto
        gasto.pagador_id = datos.get('pagador')
        gasto.cantidad = datos.get('cantidad')
        gasto.fecha = fecha
        gasto.proyecto_id = datos.get('proyecto')
        db.session.commit()
        return gasto.data, HTTPStatus.OK

    # ELIMINA EL GASTO
    def delete(self, gasto_id):
        gasto = Gasto.get_by_id(gasto_id)
        if gasto is None:
            return {'message': 'Gasto no encontrado'}, HTTPStatus.NOT_FOUND
        db.session.delete(gasto)
        db.session.commit()
        return {'message': 'Gasto eliminado'}, HTTPStatus.OK
