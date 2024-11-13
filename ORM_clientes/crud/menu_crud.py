# Importamos las herramientas necesarias para manejar sesiones de base de datos y la clase Menú
from sqlalchemy.orm import Session
from models import Menu

# Función para crear un nuevo menú en la base de datos
def crear_menu(db: Session, nombre: str, descripcion: str, ingredientes: list):
    """
    Crea un nuevo menú en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        nombre (str): Nombre del menú.
        descripcion (str): Descripción del menú.
        ingredientes (list): Lista de ingredientes asociados al menú.
    
    Returns:
        Menu: Menú recién creado.
    """
    nuevo_menu = Menu(nombre=nombre, descripcion=descripcion, ingredientes=ingredientes)
    db.add(nuevo_menu)
    db.commit()
    db.refresh(nuevo_menu)
    return nuevo_menu

# Función para obtener todos los menús registrados en la base de datos
def obtener_menus(db: Session):
    """
    Obtiene todos los menús registrados en la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
    
    Returns:
        list: Lista de menús.
    """
    return db.query(Menu).all()

# Función para obtener un menú específico por su ID
def obtener_menu_por_id(db: Session, menu_id: int):
    """
    Obtiene un menú específico por su ID.
    
    Args:
        db (Session): Sesión de base de datos.
        menu_id (int): ID del menú.
    
    Returns:
        Menu: Menú correspondiente al ID, o None si no se encuentra.
    """
    return db.query(Menu).filter(Menu.id == menu_id).first()

# Función para actualizar un menú existente
def actualizar_menu(db: Session, menu_id: int, nombre: str = None, descripcion: str = None, ingredientes: list = None):
    """
    Actualiza los datos de un menú existente.
    
    Args:
        db (Session): Sesión de base de datos.
        menu_id (int): ID del menú a actualizar.
        nombre (str, optional): Nuevo nombre del menú.
        descripcion (str, optional): Nueva descripción del menú.
        ingredientes (list, optional): Nueva lista de ingredientes.
    
    Returns:
        Menu: Menú actualizado, o None si no se encuentra.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu:  # Verificamos si el menú existe
        if nombre:
            menu.nombre = nombre
        if descripcion:
            menu.descripcion = descripcion
        if ingredientes is not None:
            menu.ingredientes = ingredientes
        db.commit()
        db.refresh(menu)
    return menu

# Función para eliminar un menú de la base de datos
def eliminar_menu(db: Session, menu_id: int):
    """
    Elimina un menú de la base de datos.
    
    Args:
        db (Session): Sesión de base de datos.
        menu_id (int): ID del menú a eliminar.
    
    Returns:
        Menu: Menú eliminado, o None si no se encuentra.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu:  # Verificamos si el menú existe
        db.delete(menu)
        db.commit()
    return menu

