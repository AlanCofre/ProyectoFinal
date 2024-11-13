# Importamos las herramientas necesarias para manejar sesiones de base de datos y la clase Ingrediente
from sqlalchemy.orm import Session
from models import Ingrediente

# Función para crear un nuevo ingrediente en la base de datos
def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad_medida: str):
    # Creamos una instancia de la clase Ingrediente con los datos proporcionados
    nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad_medida=unidad_medida)
    # Agregamos el nuevo ingrediente a la sesión de la base de datos
    db.add(nuevo_ingrediente)
    # Confirmamos la transacción para guardar el ingrediente en la base de datos
    db.commit()
    # Actualizamos la instancia para reflejar el ID generado en la base de datos
    db.refresh(nuevo_ingrediente)
    # Retornamos el ingrediente recién creado
    return nuevo_ingrediente

# Función para obtener todos los ingredientes registrados en la base de datos
def obtener_ingredientes(db: Session):
    # Realizamos una consulta para obtener todos los registros de la tabla de ingredientes
    return db.query(Ingrediente).all()

# Función para obtener un ingrediente específico por su ID
def obtener_ingrediente_por_id(db: Session, ingrediente_id: int):
    # Realizamos una consulta para buscar un ingrediente cuyo ID coincida con el proporcionado
    return db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()

# Función para actualizar los datos de un ingrediente existente
def actualizar_ingrediente(db: Session, ingrediente_id: int, nombre: str = None, tipo: str = None, cantidad: float = None, unidad_medida: str = None):
    # Buscamos el ingrediente que se desea actualizar
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if ingrediente:  # Verificamos si el ingrediente existe
        # Actualizamos los atributos si se proporcionan nuevos valores
        if nombre:
            ingrediente.nombre = nombre
        if tipo:
            ingrediente.tipo = tipo
        if cantidad is not None:
            ingrediente.cantidad = cantidad
        if unidad_medida:
            ingrediente.unidad_medida = unidad_medida
        # Confirmamos los cambios realizados en la base de datos
        db.commit()
        # Actualizamos la instancia para reflejar los cambios
        db.refresh(ingrediente)
    # Retornamos el ingrediente actualizado o None si no se encontró
    return ingrediente

# Función para eliminar un ingrediente de la base de datos
def eliminar_ingrediente(db: Session, ingrediente_id: int):
    # Buscamos el ingrediente a eliminar
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if ingrediente:  # Verificamos si el ingrediente existe
        # Eliminamos el ingrediente de la sesión de la base de datos
        db.delete(ingrediente)
        # Confirmamos la transacción para aplicar la eliminación
        db.commit()
    # Retornamos el ingrediente eliminado o None si no se encontró
    return ingrediente

