from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.modelosGeneral import Usuario
from extensiones import db

class UsuarioListResource(Resource):
    # DEVUELVE LISTA DE USUARIOS
    def get(self):
        usuarios = Usuario.query.all()
        datos = [usuario.data for usuario in usuarios]
        return datos, HTTPStatus.OK

    # CREA UN NUEVO USUARIO
    def post(self):
        datos = request.get_json()
        nombre_usuario = datos.get('nombre')
        
        # Verificar si ya existe un usuario con el mismo nombre
        if Usuario.get_by_nombre(nombre_usuario):
            return {'message': 'Ya existe un usuario con ese nombre.'}, HTTPStatus.BAD_REQUEST

        usuario = Usuario(
            nombre=nombre_usuario,
            password=datos.get('password')
        )
        usuario.guardar()
        return usuario.data, HTTPStatus.CREATED

class UsuarioResource(Resource):
    # DEVUELVE UN USUARIO
    def get(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'Usuario no encontrado'}, HTTPStatus.NOT_FOUND
        return usuario.data, HTTPStatus.OK

    # ACTUALIZA EL USUARIO
    def put(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'Usuario no encontrado'}, HTTPStatus.NOT_FOUND
        
        datos = request.get_json()
        usuario.nombre = datos.get('nombre')
        usuario.password = datos.get('password')
        usuario.guardar()
        
        # No es necesario devolver el usuario actualizado, ya se puede acceder a él a través de su ID
        return usuario.data, HTTPStatus.OK

    # ELIMINA EL USUARIO
    def delete(self, usuario_id):
        usuario = Usuario.get_by_id(usuario_id)
        if usuario is None:
            return {'message': 'Usuario no encontrado'}, HTTPStatus.NOT_FOUND
        
        db.session.delete(usuario)
        db.session.commit()
        return {'message': 'Usuario eliminado'}, HTTPStatus.OK
