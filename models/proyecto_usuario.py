from extensiones import db

class ProyectoUsuario(db.Model):
    __tablename__ = 'proyectos_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer)
    usuario_id = db.Column(db.Integer)
    

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    @classmethod
    def get_by_proyecto_id(cls, proyecto_id):
        return cls.query.filter_by(proyecto_id=proyecto_id).first()
    
    @classmethod
    def get_by_usuario_id(cls, usuario_id):
        return cls.query.filter_by(usuario_id=usuario_id).first()

    @classmethod
    def get_all_proyectos_usuarios(cls):
        proyectos_usuarios = ProyectoUsuario.query.all()
        resultados = []
        for proyecto_usuario in proyectos_usuarios:
            resultados.append({
                'id': proyecto_usuario.id,
                'proyecto_id': proyecto_usuario.proyecto_id,
                'usuario_id': proyecto_usuario.usuario_id
            })
        return resultados
    
    @classmethod
    def get_by_proyecto(cls, proyecto_id):
        proyectos_usuarios = ProyectoUsuario.query.filter_by(proyecto_id=proyecto_id).all()
        resultados = []
        for proyecto_usuario in proyectos_usuarios:
            resultados.append({
                'id': proyecto_usuario.id,
                'proyecto_id': proyecto_usuario.proyecto_id,
                'usuario_id': proyecto_usuario.usuario_id
            })
        return resultados

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'usuario_id' : self.usuario_id
        }