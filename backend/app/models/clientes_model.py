from app import db

class Cliente(db.Model):
    __tablename__ = 'Clientes'

    id                   = db.Column('Id', db.Integer, primary_key=True)
    numero_cliente       = db.Column('NumeroCliente', db.Integer, unique=True, nullable=False)
    codigo_cliente       = db.Column('CodigoCliente', db.String(10), unique=True, nullable=False)
    nombre_contacto      = db.Column('NombreContacto', db.String(200), nullable=False)
    nombre_negocio       = db.Column('NombreNegocio', db.String(200))
    departamento_id      = db.Column('DepartamentoId', db.Integer, db.ForeignKey('Departamentos.Id'), nullable=False)
    municipio_id         = db.Column('MunicipioId', db.Integer, db.ForeignKey('Municipios.Id'), nullable=False)
    direccion            = db.Column('Direccion', db.Text)
    nit                  = db.Column('Nit', db.String(15))
    encargado_bodega     = db.Column('EncargadoBodega', db.String(100))
    telefono             = db.Column('Telefono', db.String(20))
    tipo_venta_autoriz   = db.Column(
        'TipoVentaAutorizado',
        db.Enum('Credito','Contado','Ambas', name='tipo_venta'),
        nullable=False
    )
    observaciones        = db.Column('Observaciones', db.Text)
    fecha_creacion       = db.Column('FechaCreacion', db.DateTime, server_default=db.func.now())
    fecha_modificacion   = db.Column('FechaModificacion', db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    usuario_creacion     = db.Column('UsuarioCreacion', db.String(50))
    usuario_modificacion = db.Column('UsuarioModificacion', db.String(50))
    estado               = db.Column('Estado', db.Boolean, default=True)
