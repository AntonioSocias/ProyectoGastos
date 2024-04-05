from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.parte import Parte
from extensiones import db

class ParteListResource(Resource):
    # DEVUELVE LISTA DE PARTES
    def get(self):
        partes = Parte.query.all()
        datos = [parte.data for parte in partes]
        return datos, HTTPStatus.OK

    # CREA UN NUEVO PARTE
    def post(self):
        datos = request.get_json()
        parte = Parte(
            apartamento=datos.get('apartamento'),
            operador = datos.get('operador'),
            prioridad = datos.get('prioridad'),
            fecha = datos.get('fecha'),
            descripcion = datos.get('descripcion'),
            foto = datos.get('foto')
        )
        parte.guardar()
        return parte.data, HTTPStatus.CREATED

class ParteResource(Resource):
    # DEVUELVE UN PARTE
    def get(self, parte_id):
        parte = Parte.get_by_id(parte_id)
        if parte is None:
            return {'message': 'Parte no encontrado'}, HTTPStatus.NOT_FOUND
        return parte.data, HTTPStatus.OK

    # ACTUALIZA EL PARTE
    def put(self, parte_id):
        parte = Parte.get_by_id(parte_id)
        if parte is None:
            return {'message': 'Parte no encontrado'}, HTTPStatus.NOT_FOUND
        
        datos = request.get_json()
        parte.apartamento=datos.get('apartamento'),
        parte.operador = datos.get('operador'),
        parte.prioridad = datos.get('prioridad'),
        parte.fecha = datos.get('fecha'),
        parte.descripcion = datos.get('descripcion'),
        parte.foto = datos.get('foto')
        parte.guardar()
        
        # No es necesario devolver el parte actualizado, ya se puede acceder a él a través de su ID
        return parte.data, HTTPStatus.OK

    # ELIMINA EL PARTE
    def delete(self, parte_id):
        parte = Parte.get_by_id(parte_id)
        if parte is None:
            return {'message': 'Parte no encontrado'}, HTTPStatus.NOT_FOUND
        
        db.session.delete(parte)
        db.session.commit()
        return {'message': 'Parte eliminado'}, HTTPStatus.OK
