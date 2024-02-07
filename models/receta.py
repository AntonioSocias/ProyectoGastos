from extensiones import db

class Receta(db.Model):
    __tablename__ = 'recetas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    raciones = db.Column(db.Integer)
    tiempo = db.Column(db.Integer)
    pasos = db.Column(db.String(1000))
    es_publicada = db.Column(db.Boolean(), default=False)

    @classmethod
    def get_by_nombre(cls, nombre):
        return cls.query.filter_by(name=nombre).first()

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
            'name': self.name,
            'descripcion': self.descripcion,
            'raciones': self.raciones,
            'tiempo': self.tiempo,
            'pasos': self.pasos,
            'es_publicada': self.es_publicada
        }
