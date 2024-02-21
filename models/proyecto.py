from extensiones import db

class Proyecto(db.Model):
    __tablename__ = 'proyectos'
    id = db.Column(db.Integer, primary_key=True)
    administrador = db.Column(db.Integer, nullable=False)
    moneda = db.Column(db.Integer, nullable=False)
    total_gastos = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
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
            #casteo a float ya que JSON no funciona con Decimal
            'total_gastos': float(self.total_gastos),
            'titulo': self.titulo,
            'descripcion': self.descripcion
        }
