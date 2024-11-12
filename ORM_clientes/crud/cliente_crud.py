# Importamos las herramientas necesarias para manejar sesiones de base de datos y la clase Cliente
from sqlalchemy.orm import Session
from models import Cliente

# Función para crear un nuevo cliente en la base de datos
def crear_cliente(db: Session, nombre: str, correo: str):
    # Creamos una instancia de la clase Cliente con los datos proporcionados
    nuevo_cliente = Cliente(nombre=nombre, correo=correo)
    # Agregamos el nuevo cliente a la sesión de la base de datos
    db.add(nuevo_cliente)
    # Confirmamos la transacción para guardar el cliente en la base de datos
    db.commit()
    # Actualizamos la instancia para reflejar el ID generado en la base de datos
    db.refresh(nuevo_cliente)
    # Retornamos el cliente recién creado
    return nuevo_cliente

# Función para obtener todos los clientes registrados en la base de datos
def obtener_clientes(db: Session):
    # Realizamos una consulta para obtener todos los registros de la tabla de clientes
    return db.query(Cliente).all()

# Función para obtener un cliente específico por su ID
def obtener_cliente_por_id(db: Session, cliente_id: int):
    # Realizamos una consulta para buscar un cliente cuyo ID coincida con el proporcionado
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

# Función para actualizar los datos de un cliente existente
def actualizar_cliente(db: Session, cliente_id: int, nombre: str = None, correo: str = None):
    # Buscamos el cliente que se desea actualizar
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:  # Verificamos si el cliente existe
        # Actualizamos los atributos si se proporcionan nuevos valores
        if nombre:
            cliente.nombre = nombre
        if correo:
            cliente.correo = correo
        # Confirmamos los cambios realizados en la base de datos
        db.commit()
        # Actualizamos la instancia para reflejar los cambios
        db.refresh(cliente)
    # Retornamos el cliente actualizado o None si no se encontró
    return cliente

# Función para eliminar un cliente de la base de datos
def eliminar_cliente(db: Session, cliente_id: int):
    # Buscamos el cliente a eliminar
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:  # Verificamos si el cliente existe
        # Eliminamos el cliente de la sesión de la base de datos
        db.delete(cliente)
        # Confirmamos la transacción para aplicar la eliminación
        db.commit()
    # Retornamos el cliente eliminado o None si no se encontró
    return cliente
