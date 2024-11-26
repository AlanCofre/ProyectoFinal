import matplotlib.pyplot as plt
from database import session  # Asume que tienes una sesión activa de SQLAlchemy
from models import Pedido, Cliente, Ingrediente  # Importa tus modelos

# Función para ventas por fecha
def graficar_ventas_por_fecha():
    """
    Genera un gráfico de barras con las ventas agrupadas por fecha.
    """
    # Consulta datos de la base
    datos = session.query(Pedido.fecha, Pedido.total).all()
    fechas = [d[0] for d in datos]
    totales = [d[1] for d in datos]

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.bar(fechas, totales, color='blue', alpha=0.7)
    plt.xlabel("Fechas")
    plt.ylabel("Ventas Totales")
    plt.title("Ventas por Fecha")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Función para distribución de menús
def graficar_menus_mas_comprados():
    """
    Genera un gráfico de torta con la distribución de menús más comprados.
    """
    # Ejemplo: Consulta en base al modelo Pedido
    datos = session.query(Pedido.descripcion, Pedido.cantidad).all()
    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    # Graficar
    plt.figure(figsize=(8, 8))
    plt.pie(cantidades, labels=nombres, autopct='%1.1f%%', startangle=140)
    plt.title("Menús Más Comprados")
    plt.axis('equal')
    plt.show()

# Función para uso de ingredientes
def graficar_uso_ingredientes():
    """
    Genera un gráfico de barras horizontales para visualizar el uso de ingredientes.
    """
    datos = session.query(Ingrediente.nombre, Ingrediente.cantidad).all()
    nombres = [d[0] for d in datos]
    cantidades = [d[1] for d in datos]

    # Graficar
    plt.figure(figsize=(10, 6))
    plt.barh(nombres, cantidades, color='green', alpha=0.7)
    plt.xlabel("Cantidad Usada")
    plt.ylabel("Ingredientes")
    plt.title("Uso de Ingredientes")
    plt.tight_layout()
    plt.show()

