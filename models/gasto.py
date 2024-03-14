from extensiones import db

class Gasto(db.Model):
    __tablename__ = 'gastos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    pagador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    # Relación con la tabla proyectos (se infiere automáticamente)
    proyecto = db.relationship('Proyecto', backref='gastos_proyecto')
    
    # Relación con la tabla usuarios (se infiere automáticamente)
    pagador = db.relationship('Usuario', backref='gasto_pagado')

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_titulo(cls, titulo):
        return cls.query.filter_by(titulo=titulo).first()
    
    @classmethod
    def get_all_by_proyecto(cls, proyecto_id):
        return cls.query.filter_by(proyecto_id=proyecto_id).all()  # Corregido para filtrar por proyecto_id en lugar de proyecto

    def guardar(self):
        db.session.add(self)
        db.session.commit()


    @property
    def data(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'cantidad': float(self.cantidad),
            'fecha': self.fecha.isoformat(),
            'proyecto_id' : self.proyecto_id,  # Corregido para devolver proyecto_id en lugar de proyecto
            'pagador_id': self.pagador_id,     # Corregido para devolver pagador_id en lugar de pagador
        }
