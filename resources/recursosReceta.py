from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.receta import Receta

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
