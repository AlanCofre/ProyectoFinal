from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    ForeignKey,
    DateTime,
    Table,
    create_engine,
    DECIMAL,
)
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime

# Configuración base de SQLAlchemy
DATABASE_URL = "mysql+pymysql://user:password@localhost/restaurante"
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tabla de relación muchos a muchos entre Menús e Ingredientes
menu_ingredientes = Table(
    "menu_ingredientes",
    Base.metadata,
    Column("id_menu", Integer, ForeignKey("menus.id_menu", ondelete="CASCADE"), primary_key=True),
    Column("id_ingrediente", Integer, ForeignKey("ingredientes.id_ingrediente", ondelete="CASCADE"), primary_key=True),
    Column("cantidad", Float, nullable=False),  # Permite valores decimales para cantidades fraccionadas
)

# Tabla de relación muchos a muchos entre Pedidos y Menús
pedido_menus = Table(
    "pedido_menus",
    Base.metadata,
    Column("id_pedido", Integer, ForeignKey("pedidos.id_pedido", ondelete="CASCADE"), primary_key=True),
    Column("id_menu", Integer, ForeignKey("menus.id_menu", ondelete="CASCADE"), primary_key=True),
    Column("cantidad", Integer, nullable=False),
)

# Tabla Clientes
class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

# Tabla Ingredientes
class Ingrediente(Base):
    __tablename__ = "ingredientes"

    id_ingrediente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    tipo = Column(String(50), nullable=False)  # El campo ahora es obligatorio
    cantidad = Column(Float, nullable=False)
    unidad_medida = Column(String(20), nullable=False)

    menus = relationship("Menu", secondary=menu_ingredientes, back_populates="ingredientes")

# Tabla Menús
class Menu(Base):
    __tablename__ = "menus"

    id_menu = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)  # El campo ahora es obligatorio

    ingredientes = relationship("Ingrediente", secondary=menu_ingredientes, back_populates="menus")
    pedidos = relationship("Pedido", secondary=pedido_menus, back_populates="menus")

# Tabla Pedidos
class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente", ondelete="CASCADE"), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    menus = relationship("Menu", secondary=pedido_menus, back_populates="pedidos")

# Crear las tablas en la base de datos
def init_db():
    """
    Inicializa la base de datos creando las tablas definidas.
    """
    Base.metadata.create_all(engine)

# Sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
