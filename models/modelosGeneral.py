from extensiones import db

class Moneda(db.Model):
    __tablename__ = 'Monedas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    simbolo = db.Column(db.String(5), nullable=False)

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
            'simbolo': self.simbolo
        }

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla proyectos (administrador)
    proyectos_administrados = db.relationship('Proyecto', backref='administrador', foreign_keys='Proyecto.administrador_id')
    
    # Relación con la tabla gastos (pagador)
    gastos_participados = db.relationship('Gasto', backref='pagador', foreign_keys='Gasto.pagador_id')
    

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

class Gasto(db.Model):
    __tablename__ = 'Gastos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('Proyectos.id'), nullable=False)
    pagador_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    
    # Relación con la tabla proyectos (se infiere automáticamente)
    proyecto = db.relationship('Proyecto', backref='gastos')
    
    # Relación con la tabla usuarios (se infiere automáticamente)
    pagador = db.relationship('Usuario', backref='gastos_pagado')

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
    
class Proyecto(db.Model):
    __tablename__ = 'Proyectos'
    id = db.Column(db.Integer, primary_key=True)
    administrador_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)
    moneda_id = db.Column(db.Integer, db.ForeignKey('Monedas.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    
    # Relaciones
    administrador_proyecto = db.relationship('Usuario', backref='proyectos_administrados')
    moneda = db.relationship('Moneda', backref='proyectos')
    
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
            'administrador_id': self.administrador_id,
            'moneda_id': self.moneda_id,
            'titulo': self.titulo,
            'descripcion': self.descripcion
        }

"""
TABLAS DE RELACIONES
"""
class GastoUsuario(db.Model):
    __tablename__ = 'GastosUsuarios'
    id = db.Column(db.Integer, primary_key=True)
    gasto_id = db.Column(db.Integer, db.ForeignKey('Gastos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)

    # Relaciones
    gasto = db.relationship('Gasto', backref='usuarios_gastos')
    usuario = db.relationship('Usuario', backref='gastos_usuarios')

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
    
class ProyectoUsuario(db.Model):
    __tablename__ = 'ProyectosUsuarios'
    id = db.Column(db.Integer, primary_key=True)
    proyecto_id = db.Column(db.Integer, db.ForeignKey('Proyectos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'), nullable=False)

    # Relaciones
    proyecto = db.relationship('Proyecto', backref='usuarios_proyecto')
    usuario = db.relationship('Usuario', backref='proyectos_usuario')

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
            'proyecto_id': self.proyecto_id,
            'usuario_id': self.usuario_id
        }
    
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