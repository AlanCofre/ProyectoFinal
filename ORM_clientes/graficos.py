import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class GeneradorGraficos:
    def __init__(self, parent):
        """Inicializa la clase y configura los gráficos dentro del contenedor `parent`."""
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz para los gráficos."""
        frame = ctk.CTkFrame(self.parent)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Botones para generar gráficos
        ctk.CTkButton(frame, text="Gráfico de Barras", command=self.generar_grafico_barras).pack(pady=10)
        ctk.CTkButton(frame, text="Gráfico de Tortas", command=self.generar_grafico_tortas).pack(pady=10)

        # Contenedor de gráficos
        self.grafico_frame = ctk.CTkFrame(frame)
        self.grafico_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def limpiar_grafico(self):
        """Limpia el contenido del contenedor de gráficos."""
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

    def generar_grafico_barras(self):
        """Genera un gráfico de barras con datos de prueba."""
        self.limpiar_grafico()

        # Datos de prueba
        labels = ['Ingrediente 1', 'Ingrediente 2', 'Ingrediente 3']
        valores = [random.randint(10, 50) for _ in labels]

        # Crear el gráfico
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(labels, valores, color='skyblue')
        ax.set_title("Gráfico de Barras")
        ax.set_ylabel("Cantidad")
        ax.set_xlabel("Ingredientes")

        # Mostrar el gráfico
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def generar_grafico_tortas(self):
        """Genera un gráfico de tortas con datos de prueba."""
        self.limpiar_grafico()

        # Datos de prueba
        labels = ['Ingrediente A', 'Ingrediente B', 'Ingrediente C']
        valores = [random.randint(10, 50) for _ in labels]

        # Crear el gráfico
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.pie(valores, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title("Gráfico de Tortas")

        # Mostrar el gráfico
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
