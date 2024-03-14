from extensiones import db

class GastoUsuario(db.Model):
    __tablename__ = 'GastosUsuarios'
    id = db.Column(db.Integer, primary_key=True)
    gasto_id = db.Column(db.Integer, db.ForeignKey('gastos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relaciones
    gasto_id = db.relationship('Gasto', backref='gastos_usuarios')
    usuario_id = db.relationship('Usuario', backref='usuarios_gastos')

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
            'gasto_id': self.gasto_id,
            'usuario_id': self.usuario_id
        }
