from extensiones import db
from models import moneda, gasto, usuario

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    administrador = db.relationship('Usuario', backref='proyecto')
    moneda = db.relationship('Moneda', backref='proyecto')
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).first()
    

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'administrador': self.administrador,
            'moneda': self.moneda,
            'titulo': self.titulo,
            'descripcion': self.descripcion
        }
