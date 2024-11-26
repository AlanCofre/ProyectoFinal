from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Modelo de Cliente
class Cliente(Base):
    __tablename__ = 'clientes'

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    direccion = Column(String(255), nullable=True)

    pedidos = relationship("Pedido", back_populates="cliente", cascade="all, delete-orphan")

# Modelo de Ingrediente
class Ingrediente(Base):
    __tablename__ = 'ingredientes'

    id_ingrediente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)
    tipo = Column(String(50), nullable=False)
    cantidad = Column(Float, nullable=False)  # Cambiado a Float para cantidades fraccionarias
    unidad_medida = Column(String(20), nullable=False)

    menus = relationship("Menu", secondary="menu_ingredientes", back_populates="ingredientes")

# Modelo de Menú
class Menu(Base):
    __tablename__ = 'menus'

    id_menu = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)

    ingredientes = relationship("Ingrediente", secondary="menu_ingredientes", back_populates="menus")
    pedidos = relationship("Pedido", secondary="pedido_menus", back_populates="menus")

# Tabla intermedia: Relación Menú - Ingredientes
class MenuIngrediente(Base):
    __tablename__ = 'menu_ingredientes'

    id_menu = Column(Integer, ForeignKey('menus.id_menu', ondelete="CASCADE"), primary_key=True)
    id_ingrediente = Column(Integer, ForeignKey('ingredientes.id_ingrediente', ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Float, nullable=False)

# Modelo de Pedido
class Pedido(Base):
    __tablename__ = 'pedidos'

    id_pedido = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('clientes.id_cliente', ondelete="CASCADE"), nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    menus = relationship("Menu", secondary="pedido_menus", back_populates="pedidos")

# Tabla intermedia: Relación Pedido - Menús
class PedidoMenu(Base):
    __tablename__ = 'pedido_menus'

    id_pedido = Column(Integer, ForeignKey('pedidos.id_pedido', ondelete="CASCADE"), primary_key=True)
    id_menu = Column(Integer, ForeignKey('menus.id_menu', ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Integer, nullable=False)

