from extensiones import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    administrador = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    moneda_id = db.Column(db.Integer, db.ForeignKey('moneda.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    
    # Relaciones
    administrador = db.relationship('Usuario', backref='proyectos', foreign_keys=[administrador])
    moneda = db.relationship('Moneda', backref='proyectos', foreign_keys=[moneda_id])

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
