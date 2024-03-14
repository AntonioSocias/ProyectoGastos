from extensiones import db
"""
class ProyectoUsuario(db.Model):
    __tablename__ = 'proyectos_usuarios'
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relaciones
    proyecto_id = db.relationship('Proyecto', backref='usuarios_proyecto')
    usuario_id = db.relationship('Usuario', backref='proyectos_usuario')

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        return {
            'id': self.id,
            'proyecto_id': self.proyecto_id,
            'usuario_id': self.usuario_id
        }
"""
