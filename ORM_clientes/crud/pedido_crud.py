# archivo: crud/pedido_crud.py
from sqlalchemy.orm import Session
from models import Pedido

class PedidoCRUD:
    def __init__(self, db: Session):
        self.db = db

    def crear_pedido(self, descripcion: str, total: float, fecha: str, cantidad_menus: int, cliente_id: int):
        nuevo_pedido = Pedido(descripcion=descripcion, total=total, fecha=fecha, cantidad_menus=cantidad_menus, cliente_id=cliente_id)
        self.db.add(nuevo_pedido)
        self.db.commit()
        self.db.refresh(nuevo_pedido)
        return nuevo_pedido

    def obtener_pedidos(self):
        return self.db.query(Pedido).all()

    def obtener_pedido_por_id(self, pedido_id: int):
        return self.db.query(Pedido).filter(Pedido.id == pedido_id).first()

    def actualizar_pedido(self, pedido_id: int, descripcion: str = None, total: float = None, fecha: str = None, cantidad_menus: int = None):
        pedido = self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            if descripcion:
                pedido.descripcion = descripcion
            if total is not None:
                pedido.total = total
            if fecha:
                pedido.fecha = fecha
            if cantidad_menus is not None:
                pedido.cantidad_menus = cantidad_menus
            self.db.commit()
            self.db.refresh(pedido)
        return pedido

    def eliminar_pedido(self, pedido_id: int):
        pedido = self.db.query(Pedido).filter(Pedido.id == pedido_id).first()
        if pedido:
            self.db.delete(pedido)
            self.db.commit()
        return pedido
