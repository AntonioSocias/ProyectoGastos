from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.usuario import Usuario
from extensiones import db
#import json OPCION PARA TENER TILDES

#PARTE A MODIFICAR
class UsuarioListResource(Resource):
	#DEVUELVE LISTA DE USUARIOS
    def get(self):
        datos = []
        usuarios_list = Usuario.query.all()
        for usuario in usuarios_list:
            datos.append(usuario.data)
        return datos, HTTPStatus.OK

    #CREA UN NUEVO USUARIO
    def post(self):
        datos = request.get_json()
        nombre_usuario = datos.get('nombre')
        if Usuario.get_by_nombre(nombre_usuario):
            return {'message': 'Ya existe un usuario con ese nombre.'}, HTTPStatus.BAD_REQUEST

        usuario = Usuario(
        	#id se genera automáticamente
            nombre=nombre_usuario
        )
        usuario.guardar()
        return usuario.data, HTTPStatus.CREATED

class UsuarioResource(Resource):
	#DEVUELVE UN USUARIO
    def get(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'Usuario no encontrada'}, HTTPStatus.NOT_FOUND
        return usuario.data, HTTPStatus.OK

    #ACTUALIZA EL USUARIO
    def put(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'usuario no encontrada'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        usuario.nombre = datos.get('nombre')
        usuario.guardar()
        #AL ACABAR DEVUELVO EL USUARIO/QUIZAS NO TENGA QUE HACERLO
        return usuario.data, HTTPStatus.OK
    #ELIMINA EL USUARIO
    def delete(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'Usuario no encontrada'}, HTTPStatus.NOT_FOUND
        db.session.delete(usuario)
        db.session.commit()
		#DEBERIA ELIMINAR EL PASO DE MESSAGE?????
        return {'message': 'Usuario eliminado'}, HTTPStatus.OK