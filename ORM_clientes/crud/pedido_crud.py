# Importamos las herramientas necesarias para manejar sesiones de base de datos y la clase Pedido
from sqlalchemy.orm import Session
from models import Pedido

# Función para crear un nuevo pedido en la base de datos
def crear_pedido(db: Session, descripcion: str, total: float, fecha: str, cantidad_menus: int, cliente_id: int):
    """
    Crea un nuevo pedido en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        descripcion (str): Descripción del pedido.
        total (float): Total del pedido.
        fecha (str): Fecha de creación del pedido.
        cantidad_menus (int): Cantidad de menús en el pedido.
        cliente_id (int): ID del cliente que realiza el pedido.
    
    Returns:
        Pedido: Pedido recién creado.
    """
    nuevo_pedido = Pedido(descripcion=descripcion, total=total, fecha=fecha, cantidad_menus=cantidad_menus, cliente_id=cliente_id)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return nuevo_pedido

# Función para obtener todos los pedidos registrados en la base de datos
def obtener_pedidos(db: Session):
    """
    Obtiene todos los pedidos registrados en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
    
    Returns:
        list: Lista de pedidos.
    """
    return db.query(Pedido).all()

# Función para obtener un pedido específico por su ID
def obtener_pedido_por_id(db: Session, pedido_id: int):
    """
    Obtiene un pedido específico por su ID.
    
    Args:
        db (Session): Sesión de base de datos.
        pedido_id (int): ID del pedido.
    
    Returns:
        Pedido: Pedido correspondiente al ID, o None si no se encuentra.
    """
    return db.query(Pedido).filter(Pedido.id == pedido_id).first()

# Función para actualizar un pedido existente
def actualizar_pedido(db: Session, pedido_id: int, descripcion: str = None, total: float = None, fecha: str = None, cantidad_menus: int = None):
    """
    Actualiza los datos de un pedido existente.
    
    Args:
        db (Session): Sesión de base de datos.
        pedido_id (int): ID del pedido a actualizar.
        descripcion (str, optional): Nueva descripción del pedido.
        total (float, optional): Nuevo total del pedido.
        fecha (str, optional): Nueva fecha de creación del pedido.
        cantidad_menus (int, optional): Nueva cantidad de menús.
    
    Returns:
        Pedido: Pedido actualizado, o None si no se encuentra.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:  # Verificamos si el pedido existe
        if descripcion:
            pedido.descripcion = descripcion
        if total is not None:
            pedido.total = total
        if fecha:
            pedido.fecha = fecha
        if cantidad_menus is not None:
            pedido.cantidad_menus = cantidad_menus
        db.commit()
        db.refresh(pedido)
    return pedido

# Función para eliminar un pedido de la base de datos
def eliminar_pedido(db: Session, pedido_id: int):
    """
    Elimina un pedido de la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        pedido_id (int): ID del pedido a eliminar.
    
    Returns:
        Pedido: Pedido eliminado, o None si no se encuentra.
    """
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if pedido:  # Verificamos si el pedido existe
        db.delete(pedido)
        db.commit()
    return pedido

