from sqlalchemy.orm import Session
from models import Cliente

# Crear un nuevo cliente
def crear_cliente(db: Session, nombre: str, correo: str):
    nuevo_cliente = Cliente(nombre=nombre, correo=correo)
    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# Leer todos los clientes
def obtener_clientes(db: Session):
    return db.query(Cliente).all()

# Leer un cliente por ID
def obtener_cliente_por_id(db: Session, cliente_id: int):
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

# Actualizar un cliente
def actualizar_cliente(db: Session, cliente_id: int, nombre: str = None, correo: str = None):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        if nombre:
            cliente.nombre = nombre
        if correo:
            cliente.correo = correo
        db.commit()
        db.refresh(cliente)
    return cliente

# Eliminar un cliente
def eliminar_cliente(db: Session, cliente_id: int):
    cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
    if cliente:
        db.delete(cliente)
        db.commit()
    return cliente
