from extensiones import db

class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    proyecto = db.Column(db.Integer, nullable=False)
    pagador = db.Column(db.Integer, nullable=False)
    
    

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).first()
    
    @classmethod
    def get_by_pagador(cls, pagador):
        return cls.query.filter_by(pagador=pagador).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'cantidad': float(self.cantidad),
            #CONVIERO EL DATE A TEXTO YA QUE JSON NO ADMITE DATE
            'fecha': self.fecha.isoformat(),
            'proyecto' : self.proyecto,
            'pagador': self.pagador,           
        }