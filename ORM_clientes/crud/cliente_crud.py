# archivo: crud/cliente_crud.py
from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_cliente(self, nombre: str, correo: str):
        # Creamos una instancia de la clase Cliente con los datos proporcionados
        nuevo_cliente = Cliente(nombre=nombre, correo=correo)
        self.db.add(nuevo_cliente)
        self.db.commit()
        self.db.refresh(nuevo_cliente)
        return nuevo_cliente

    def obtener_clientes(self):
        # Obtenemos todos los clientes
        return self.db.query(Cliente).all()

    def obtener_cliente_por_id(self, cliente_id: int):
        # Obtenemos un cliente por ID
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def actualizar_cliente(self, cliente_id: int, nombre: str = None, correo: str = None):
        # Actualizamos un cliente por su ID
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            if nombre:
                cliente.nombre = nombre
            if correo:
                cliente.correo = correo
            self.db.commit()
            self.db.refresh(cliente)
        return cliente

    def eliminar_cliente(self, cliente_id: int):
        # Eliminamos un cliente por su ID
        cliente = self.db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            self.db.delete(cliente)
            self.db.commit()
        return cliente
