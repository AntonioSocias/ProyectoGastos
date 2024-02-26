from extensiones import db

class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    pagado = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_pagado(cls, pagado):
        return cls.query.filter_by(pagado=pagado).first()
    

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'pagado': self.pagado,
            #casteo a float ya que JSON no funciona con Decimal
            'cantidad': float(self.cantidad),
            'fecah': self.fecha
        }
