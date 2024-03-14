from extensiones import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relación con la tabla proyectos
    proyectos = db.relationship('Proyecto', secondary='ProyectosUsuarios', backref='usuarios')


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_nombre(cls, nombre):
        return cls.query.filter_by(nombre=nombre).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'password' : self.password
        }