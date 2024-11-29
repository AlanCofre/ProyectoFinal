import customtkinter as ctk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from fpdf import FPDF
import os
from datetime import datetime

class RestauranteApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Restaurante")
        self.geometry("900x700")

        self.stock = []  # Lista para ingredientes
        self.menus = []  # Lista para menús
        self.clientes = []  # Lista para clientes
        self.pedidos = []  # Lista para pedidos
        self.total = 0  # Total acumulado en pedidos actuales

        # Crear y configurar pestañas
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(expand=True, fill="both")

        self.tab_ingreso_ingredientes = self.tabs.add("Ingredientes")
        self.tab_menus = self.tabs.add("Menús")
        self.tab_clientes = self.tabs.add("Clientes")
        self.tab_pedido = self.tabs.add("Pedidos")
        self.tab_graficos = self.tabs.add("Gráficos")

        self.setup_ingreso_ingredientes()
        self.setup_menus()
        self.setup_clientes()
        self.setup_pedido()  
        self.setup_graficos()

    # ------------------- INGREDIENTES ------------------- #
    def setup_ingreso_ingredientes(self):
        frame = ctk.CTkFrame(self.tab_ingreso_ingredientes)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Entrada de datos
        ctk.CTkLabel(frame, text="Nombre del Ingrediente").pack(pady=5)
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame)
        self.entry_nombre_ingrediente.pack(pady=5)

        ctk.CTkLabel(frame, text="Cantidad").pack(pady=5)
        self.entry_cantidad_ingrediente = ctk.CTkEntry(frame)
        self.entry_cantidad_ingrediente.pack(pady=5)

        # Botones
        ctk.CTkButton(frame, text="Agregar Ingrediente", command=self.agregar_ingrediente).pack(pady=10)
        ctk.CTkButton(frame, text="Eliminar Ingrediente", command=self.eliminar_ingrediente).pack(pady=10)

        # Tabla de ingredientes
        self.treeview_ingredientes = ttk.Treeview(frame, columns=("Nombre", "Cantidad"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes.pack(fill="both", expand=True, padx=10, pady=10)

    def agregar_ingrediente(self):
        nombre = self.entry_nombre_ingrediente.get().strip()
        cantidad = self.entry_cantidad_ingrediente.get().strip()

        if not nombre or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Datos inválidos.")
            return

        for ing in self.stock:
            if ing["nombre"] == nombre:
                ing["cantidad"] += int(cantidad)
                self.actualizar_treeview_ingredientes()
                self.actualizar_treeview_ingredientes_menu()  # Actualizar la lista de ingredientes en Menú
                return

        self.stock.append({"nombre": nombre, "cantidad": int(cantidad)})
        self.actualizar_treeview_ingredientes()
        self.actualizar_treeview_ingredientes_menu()  # Actualizar la lista de ingredientes en Menú


    def eliminar_ingrediente(self):
        seleccion = self.treeview_ingredientes.selection()
        if seleccion:
            nombre = self.treeview_ingredientes.item(seleccion, "values")[0]
            self.stock = [ing for ing in self.stock if ing["nombre"] != nombre]
            self.actualizar_treeview_ingredientes()

    def actualizar_treeview_ingredientes(self):
        for item in self.treeview_ingredientes.get_children():
            self.treeview_ingredientes.delete(item)
        for ing in self.stock:
            self.treeview_ingredientes.insert("", "end", values=(ing["nombre"], ing["cantidad"]))

       # ------------------- MENÚS ------------------- #
    def setup_menus(self):
        frame = ctk.CTkFrame(self.tab_menus)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Entrada para nombre y descripción del menú
        ctk.CTkLabel(frame, text="Nombre del Menú").pack(pady=5)
        self.entry_nombre_menu = ctk.CTkEntry(frame)
        self.entry_nombre_menu.pack(pady=5)

        ctk.CTkLabel(frame, text="Descripción del Menú").pack(pady=5)
        self.entry_descripcion_menu = ctk.CTkEntry(frame)
        self.entry_descripcion_menu.pack(pady=5)

        # Entrada para el precio del menú
        ctk.CTkLabel(frame, text="Precio del Menú").pack(pady=5)
        self.entry_precio_menu = ctk.CTkEntry(frame)
        self.entry_precio_menu.pack(pady=5)


        # Tabla para seleccionar ingredientes
        ctk.CTkLabel(frame, text="Seleccionar Ingredientes").pack(pady=5)
        self.treeview_ingredientes_menu = ttk.Treeview(frame, columns=("Nombre", "Cantidad"), show="headings")
        self.treeview_ingredientes_menu.heading("Nombre", text="Nombre")
        self.treeview_ingredientes_menu.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes_menu.pack(fill="both", expand=True, padx=10, pady=10)

        self.actualizar_treeview_ingredientes_menu()

        # Botón para agregar el menú
        ctk.CTkButton(frame, text="Crear Menú", command=self.crear_menu).pack(pady=10)

        # Tabla para mostrar menús creados (agregamos la columna de precio)
        ctk.CTkLabel(frame, text="Menús Creados").pack(pady=5)
        self.treeview_menus = ttk.Treeview(frame, columns=("Nombre", "Descripción", "Precio"), show="headings")
        self.treeview_menus.heading("Nombre", text="Nombre")
        self.treeview_menus.heading("Descripción", text="Descripción")
        self.treeview_menus.heading("Precio", text="Precio")
        self.treeview_menus.pack(fill="both", expand=True, padx=10, pady=10)

    def actualizar_treeview_ingredientes_menu(self):
        # Limpiar la tabla de ingredientes
        for item in self.treeview_ingredientes_menu.get_children():
            self.treeview_ingredientes_menu.delete(item)

        # Mostrar los ingredientes disponibles
        for ing in self.stock:
            self.treeview_ingredientes_menu.insert("", "end", values=(ing["nombre"], ing["cantidad"]))


    def crear_menu(self):
        nombre = self.entry_nombre_menu.get().strip()
        descripcion = self.entry_descripcion_menu.get().strip()
        precio = self.entry_precio_menu.get().strip()

        if not nombre or not descripcion or not precio:
            messagebox.showerror("Error", "Debe llenar todos los campos.")
            return

        # Verificar que el precio sea un número válido
        try:
            precio = float(precio)
            if precio <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Precio inválido.")
            return

        # Obtener los ingredientes seleccionados
        seleccionados = self.treeview_ingredientes_menu.selection()
        if not seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un ingrediente.")
            return

        ingredientes_menu = []
        for item in seleccionados:
            nombre_ing = self.treeview_ingredientes_menu.item(item, "values")[0]
            cantidad_ing = self.treeview_ingredientes_menu.item(item, "values")[1]

            # Solicitar cantidad a usar
            cantidad_a_usar = self.solicitar_cantidad_ing(nombre_ing, cantidad_ing)
            if cantidad_a_usar is None:
                return  # El usuario canceló la entrada

            # Validar cantidad
            if cantidad_a_usar > int(cantidad_ing):
                messagebox.showerror("Error", f"No hay suficiente {nombre_ing}.")
                return

            ingredientes_menu.append({"nombre": nombre_ing, "cantidad": cantidad_a_usar})

        # Reducir cantidades en el inventario
        for ingrediente in ingredientes_menu:
            for ing in self.stock:
                if ing["nombre"] == ingrediente["nombre"]:
                    ing["cantidad"] -= ingrediente["cantidad"]

        # Crear el menú
        self.menus.append({"nombre": nombre, "descripcion": descripcion, "precio": precio, "ingredientes": ingredientes_menu})
        self.actualizar_treeview_ingredientes_menu()
        self.actualizar_treeview_menus()

        # Verificar que el menú se agregó
        print(f"Menús: {self.menus}")  # Verifica si el menú fue agregado

        messagebox.showinfo("Éxito", f"Menú '{nombre}' creado correctamente.")


    def actualizar_treeview_menus(self):
        for item in self.treeview_menus.get_children():
            self.treeview_menus.delete(item)
        for menu in self.menus:
            self.treeview_menus.insert("", "end", values=(menu["nombre"], menu["descripcion"], f"${menu['precio']:.2f}"))


    # ------------------- CLIENTES ------------------- #
    def setup_clientes(self):
        frame = ctk.CTkFrame(self.tab_clientes)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Nombre del Cliente").pack(pady=5)
        self.entry_nombre_cliente = ctk.CTkEntry(frame)
        self.entry_nombre_cliente.pack(pady=5)

        ctk.CTkLabel(frame, text="Correo del Cliente").pack(pady=5)
        self.entry_correo_cliente = ctk.CTkEntry(frame)
        self.entry_correo_cliente.pack(pady=5)

        ctk.CTkButton(frame, text="Registrar Cliente", command=self.registrar_cliente).pack(pady=10)

        self.treeview_clientes = ttk.Treeview(frame, columns=("Nombre", "Correo"), show="headings")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Correo", text="Correo")
        self.treeview_clientes.pack(fill="both", expand=True, padx=10, pady=10)

    def registrar_cliente(self):
        nombre = self.entry_nombre_cliente.get().strip()
        correo = self.entry_correo_cliente.get().strip()

        if not nombre or not correo:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        for cliente in self.clientes:
            if cliente["correo"] == correo:
                messagebox.showerror("Error", "El correo ya está registrado.")
                return

        self.clientes.append({"nombre": nombre, "correo": correo})
        self.actualizar_treeview_clientes()

        # Verificar que el cliente fue agregado
        print(f"Clientes: {self.clientes}")  # Verifica si el cliente fue agregado

        messagebox.showinfo("Éxito", f"Cliente '{nombre}' registrado correctamente.")


    def actualizar_treeview_clientes(self):
        for item in self.treeview_clientes.get_children():
            self.treeview_clientes.delete(item)
        for cliente in self.clientes:
            self.treeview_clientes.insert("", "end", values=(cliente["nombre"], cliente["correo"]))



  
    # ------------------- PEDIDOS ------------------- #
    def setup_pedido(self):
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabla de Menús Creados con la cantidad disponible
        ctk.CTkLabel(frame, text="Menús Creados y Cantidad Disponible").pack(pady=5)
        self.treeview_menus_disponibles = ttk.Treeview(frame, columns=("Menú", "Cantidad Disponible"), show="headings")
        self.treeview_menus_disponibles.heading("Menú", text="Menú")
        self.treeview_menus_disponibles.heading("Cantidad Disponible", text="Cantidad Disponible")
        self.treeview_menus_disponibles.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_treeview_menus_disponibles()

        # Tabla para seleccionar Clientes
        ctk.CTkLabel(frame, text="Seleccionar Cliente").pack(pady=5)
        self.treeview_clientes_select = ttk.Treeview(frame, columns=("Nombre", "Correo"), show="headings")
        self.treeview_clientes_select.heading("Nombre", text="Nombre")
        self.treeview_clientes_select.heading("Correo", text="Correo")
        self.treeview_clientes_select.pack(fill="both", expand=True, padx=10, pady=10)
        self.actualizar_treeview_clientes_select()

        # Botón para generar boleta
        ctk.CTkButton(frame, text="Generar Boleta", command=self.generar_boleta).pack(pady=10)

    def actualizar_treeview_menus_disponibles(self):
        for item in self.treeview_menus_disponibles.get_children():
            self.treeview_menus_disponibles.delete(item)

        for menu in self.menus:
            self.treeview_menus_disponibles.insert("", "end", values=(menu["nombre"], "Disponible"))

    def calcular_cantidad_menu(self, ingredientes_menu):
        # Calcula cuántos menús se pueden hacer según los ingredientes disponibles
        cantidad_disponible = float('inf')  # Inicializa con infinito
        for ingrediente in ingredientes_menu:
            for stock_ingrediente in self.stock:
                if stock_ingrediente["nombre"] == ingrediente["nombre"]:
                    cantidad_posible = stock_ingrediente["cantidad"] // ingrediente["cantidad"]
                    cantidad_disponible = min(cantidad_disponible, cantidad_posible)
        return cantidad_disponible

    def actualizar_treeview_clientes_select(self):
        for item in self.treeview_clientes_select.get_children():
            self.treeview_clientes_select.delete(item)

        # Mostrar los clientes disponibles
        for cliente in self.clientes:
            self.treeview_clientes_select.insert("", "end", values=(cliente["nombre"], cliente["correo"]))

    def generar_boleta(self):
        cliente_seleccionado = self.treeview_clientes_select.selection()
        if not cliente_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un cliente.")
            return

        cliente = self.treeview_clientes_select.item(cliente_seleccionado, "values")
        cliente_nombre = cliente[0]
        cliente_correo = cliente[1]

        # Recopilar los menús seleccionados
        menues_seleccionados = self.treeview_menus_disponibles.selection()
        if not menues_seleccionados:
            messagebox.showerror("Error", "Debe seleccionar al menos un menú.")
            return

        # Crear el PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
    
        # Título
        pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align="C")
    
        # Información del Cliente
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Cliente: {cliente_nombre}", ln=True)
        pdf.cell(200, 10, txt=f"Correo: {cliente_correo}", ln=True)
    
        # Detalles del pedido
        pdf.ln(10)
        pdf.cell(200, 10, txt="Menú(s) Pedido(s):", ln=True)
        total_pedido = 0
        for item in menues_seleccionados:
            menu_nombre = self.treeview_menus_disponibles.item(item, "values")[0]
            cantidad = 1  # Aquí podrías agregar lógica para preguntar cuántos menús
            total_pedido += cantidad * 10  # Suponiendo un precio fijo, aquí debes calcular el precio real

            pdf.cell(200, 10, txt=f"- {menu_nombre} x {cantidad} = ${cantidad * 10}", ln=True)

        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total: ${total_pedido}", ln=True)

        # Guardar el PDF
        pdf.output(f"boleta_{cliente_nombre}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf")
        messagebox.showinfo("Éxito", "Boleta generada correctamente.")


    def crear_pdf_boleta(self, boleta_texto):
        # Crear un documento PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, boleta_texto)

        # Guardar el archivo PDF
        nombre_archivo = f"boleta_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf.output(nombre_archivo)

        messagebox.showinfo("Éxito", f"Boleta generada: {nombre_archivo}")

    # ------------------- GRÁFICOS ------------------- #
    def setup_graficos(self):
        frame = ctk.CTkFrame(self.tab_graficos)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(frame, text="Selecciona un tipo de gráfico").pack(pady=10)
        self.dropdown_graficos = ctk.CTkComboBox(frame, values=["Ventas por Menú", "Ingredientes Usados"])
        self.dropdown_graficos.pack(pady=10)

        ctk.CTkButton(frame, text="Generar Gráfico", command=self.mostrar_grafico).pack(pady=10)

    def mostrar_grafico(self):
        grafico_seleccionado = self.dropdown_graficos.get()

        if grafico_seleccionado == "Ventas por Menú":
            self.graficar_ventas_por_menu()
        elif grafico_seleccionado == "Ingredientes Usados":
            self.graficar_ingredientes_usados()
        else:
            messagebox.showerror("Error", "Selecciona un tipo de gráfico.")

    def graficar_ventas_por_menu(self):
        import matplotlib.pyplot as plt

        menus = [pedido["menu"] for pedido in self.pedidos]
        cantidades = [pedido["cantidad"] for pedido in self.pedidos]

        plt.bar(menus, cantidades, color='blue')
        plt.title("Ventas por Menú")
        plt.xlabel("Menús")
        plt.ylabel("Cantidad Vendida")
        plt.show()

    def graficar_ingredientes_usados(self):
        import matplotlib.pyplot as plt

        ingredientes = [f"{ing['nombre']} - {ing['cantidad']}" for ing in self.stock]
        cantidades = [ing["cantidad"] for ing in self.stock]

        plt.pie(cantidades, labels=ingredientes, autopct="%1.1f%%")
        plt.title("Distribución de Ingredientes Usados")
        plt.show()

if __name__ == "__main__":
    app = RestauranteApp()
    app.mainloop()