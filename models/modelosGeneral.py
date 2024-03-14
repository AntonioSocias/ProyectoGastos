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
    
class Proyecto(db.Model):
    __tablename__ = 'Proyectos'
    id = db.Column(db.Integer, primary_key=True)
    administrador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    moneda_id = db.Column(db.Integer, db.ForeignKey('moneda.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.String(255))
    
    # Relaciones
    administrador_proyecto = db.relationship('Usuario', backref='proyectos_administrados_relacion', foreign_keys=[administrador_id])
    moneda = db.relationship('Moneda', backref='moneda_proyecto', foreign_keys=[moneda_id])
    
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

class Usuario(db.Model):
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    
    # Relación con la tabla proyectos (administrador)
    proyectos_administrados = db.relationship('Proyecto', backref='administrador', foreign_keys='Proyecto.administrador_id')
    
    # Relación con la tabla gastos (pagador)
    gastos_participados = db.relationship('Gasto', backref='pagador_usuarios', foreign_keys='Gasto.pagador_id')
    

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

"""
TABLAS DE RELACIONES
"""
class GastoUsuario(db.Model):
    __tablename__ = 'GastosUsuarios'
    id = db.Column(db.Integer, primary_key=True)
    gasto_id = db.Column(db.Integer, db.ForeignKey('gastos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relaciones
    gasto_id = db.relationship('Gasto', backref='gastos_usuarios')
    usuario_id = db.relationship('Usuario', backref='usuarios_gastos')

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
    proyecto_id = db.Column(db.Integer, db.ForeignKey('proyectos.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relaciones
    proyecto_id = db.relationship('Proyecto', backref='usuarios_proyecto')
    usuario_id = db.relationship('Usuario', backref='proyectos_usuario')

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