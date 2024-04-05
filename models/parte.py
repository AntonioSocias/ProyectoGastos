from extensiones import db

class Parte(db.Model):
    __tablename__ = 'partes'
    id = db.Column(db.Integer, primary_key=True)
    apartamento = db.Column(db.String(10), nullable=False)
    operador = db.Column(db.String(20), nullable=False)
    prioridad = db.Column(db.Numeric(precision=10), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    descripcion = db.Column(db.String(10), nullable=False)
    foto = db.Column(db.LargeBinary)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all_by_operador(cls, id):
        return cls.query.filter_by(id=id).all()
    @classmethod
    def get_all_by_apartamento(cls, apartamento):
        return cls.query.filter_by(apartamento=apartamento).all()
    
    @classmethod
    def get_all_by_fecha(cls, fecha):
        return cls.query.filter_by(fecha=fecha).all()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    @property
    def data(self):
        return {
            'id': self.id,
            'apartamento': self.apartamento,
            'prioridad': float(self.prioridad),
            'fecha': self.fecha.isoformat(),
            'descripcion': self.descripcion,
            'foto': self.foto  # Se añade el campo 'foto'
        }
