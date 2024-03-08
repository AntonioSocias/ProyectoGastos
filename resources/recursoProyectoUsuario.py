from ast import For
from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.proyecto_usuario import ProyectoUsuario
from extensiones import db
#import json OPCION PARA TENER TILDES

#PARTE A MODIFICAR
class ProyectosUsuariosListResource(Resource):
	#DEVUELVE LISTA DE Proyectos Usuarios
    def get(self):
        proyectos_usuarios = ProyectoUsuario.query.all()
        resultados = []
        for proyecto_usuario in proyectos_usuarios:
            resultados.append({
                'id': proyecto_usuario.id,
                'proyecto_id': proyecto_usuario.proyecto_id,
                'usuario_id': proyecto_usuario.usuario_id
            })
        return resultados

    #CREA UNA NUEVA RELACION Proyectos Usuarios
    def post(self):
        datos = request.get_json()
        usuario_id = datos.get('usuario_id')
        proyecto_id = datos.get('proyecto_id')
        if ProyectoUsuario.get_by_proyecto_id(proyecto_id) and ProyectoUsuario.get_by_usuario_id(usuario_id):
            return {'message': 'Ya existe un campo con esos valores.'}, HTTPStatus.BAD_REQUEST

        ProUsu = ProyectoUsuario(
        	#id se genera automáticamente
            usuario_id=usuario_id,
            proyecto_id=proyecto_id
        )
        ProUsu.guardar()
        return ProUsu.data, HTTPStatus.CREATED

class ProyectoUsuariosListResource(Resource):
	#DEVUELVE LISTA BASADO EN PROYECTO
    def get(self, proyecto_id):
        proyecto_usuarios = ProyectoUsuario.query.filter_by(proyecto_id=proyecto_id).all()
        resultados = []
        for proyecto_usuario in proyecto_usuarios:
            resultados.append({
                'id': proyecto_usuario.id,
                'proyecto_id': proyecto_usuario.proyecto_id,
                'usuario_id': proyecto_usuario.usuario_id
            })
        return resultados, HTTPStatus.OK

    #ACTUALIZA EL Proyectos Usuarios
    def put(self, id):
        proyecto_usuario = ProyectoUsuario.get_by_id(id)
        if proyecto_usuario is None:
            return {'message': 'Relación no encontrada'}, HTTPStatus.NOT_FOUND
        datos = request.get_json()
        proyecto_usuario.proyecto_id = datos.get('proyecto_id')
        proyecto_usuario.usuario_id = datos.get('usuario_id')
        proyecto_usuario.guardar()
        #AL ACABAR DEVUELVO EL USUARIO/QUIZAS NO TENGA QUE HACERLO
        return proyecto_usuario.data, HTTPStatus.OK
    
    #ELIMINA LA RELACION
    def delete(self, id):
        proyecto_usuario = ProyectoUsuario.get_by_id(id)
        if proyecto_usuario is None:
            return {'message': 'Relación no encontrada'}, HTTPStatus.NOT_FOUND
        db.session.delete(proyecto_usuario)
        db.session.commit()
		#DEBERIA ELIMINAR EL PASO DE MESSAGE?????
        return {'message': 'Relación eliminada'}, HTTPStatus.OK