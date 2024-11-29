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

        # Tabla para seleccionar ingredientes
        ctk.CTkLabel(frame, text="Seleccionar Ingredientes").pack(pady=5)
        self.treeview_ingredientes_menu = ttk.Treeview(frame, columns=("Nombre", "Cantidad"), show="headings")
        self.treeview_ingredientes_menu.heading("Nombre", text="Nombre")
        self.treeview_ingredientes_menu.heading("Cantidad", text="Cantidad")
        self.treeview_ingredientes_menu.pack(fill="both", expand=True, padx=10, pady=10)

        self.actualizar_treeview_ingredientes_menu()

        # Botón para agregar el menú
        ctk.CTkButton(frame, text="Crear Menú", command=self.crear_menu).pack(pady=10)

        # Tabla para mostrar menús creados
        ctk.CTkLabel(frame, text="Menús Creados").pack(pady=5)
        self.treeview_menus = ttk.Treeview(frame, columns=("Nombre", "Descripción"), show="headings")
        self.treeview_menus.heading("Nombre", text="Nombre")
        self.treeview_menus.heading("Descripción", text="Descripción")
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

        if not nombre or not descripcion:
            messagebox.showerror("Error", "Debe llenar todos los campos.")
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
        self.menus.append({"nombre": nombre, "descripcion": descripcion, "ingredientes": ingredientes_menu})
        self.actualizar_treeview_ingredientes_menu()
        self.actualizar_treeview_menus()

        messagebox.showinfo("Éxito", f"Menú '{nombre}' creado correctamente.")


    def solicitar_cantidad_ing(self, nombre, cantidad_disponible):
        # Ventana emergente para pedir cantidad
        cantidad = ctk.CTkInputDialog(
            text=f"Ingrese la cantidad de '{nombre}' (Disponible: {cantidad_disponible})",
            title="Cantidad de Ingrediente"
        )
        try:
            cantidad_ingresada = int(cantidad.get_input().strip())
            if cantidad_ingresada <= 0:
                raise ValueError("Cantidad no válida.")
            return cantidad_ingresada
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Cantidad ingresada no válida.")
            return None

    def actualizar_treeview_menus(self):
        for item in self.treeview_menus.get_children():
            self.treeview_menus.delete(item)
        for menu in self.menus:
            self.treeview_menus.insert("", "end", values=(menu["nombre"], menu["descripcion"]))

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

    def actualizar_treeview_clientes(self):
        for item in self.treeview_clientes.get_children():
            self.treeview_clientes.delete(item)
        for cliente in self.clientes:
            self.treeview_clientes.insert("", "end", values=(cliente["nombre"], cliente["correo"]))

    # ------------------- PEDIDOS ------------------- #
    def setup_pedido(self):
        frame = ctk.CTkFrame(self.tab_pedido)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Dropdown para seleccionar cliente
        ctk.CTkLabel(frame, text="Cliente").pack(pady=5)
        self.dropdown_cliente_pedido = ctk.CTkComboBox(frame, values=[c["nombre"] for c in self.clientes])
        self.dropdown_cliente_pedido.pack(pady=5)

        # Dropdown para seleccionar menú
        ctk.CTkLabel(frame, text="Menú").pack(pady=5)
        self.dropdown_menu_pedido = ctk.CTkComboBox(frame, values=[m["nombre"] for m in self.menus])
        self.dropdown_menu_pedido.pack(pady=5)

        # Botones para agregar menús al pedido
        ctk.CTkButton(frame, text="Agregar al Pedido", command=self.agregar_al_pedido).pack(pady=10)

        # Tabla para mostrar el pedido
        self.treeview_pedido = ttk.Treeview(frame, columns=("Menú", "Cantidad", "Precio"), show="headings")
        self.treeview_pedido.heading("Menú", text="Menú")
        self.treeview_pedido.heading("Cantidad", text="Cantidad")
        self.treeview_pedido.heading("Precio", text="Precio")
        self.treeview_pedido.pack(fill="both", expand=True, padx=10, pady=10)

        # Botón para generar boleta
        ctk.CTkButton(frame, text="Generar Boleta", command=self.generar_boleta).pack(pady=10)

    def agregar_al_pedido(self):
        menu_seleccionado = self.dropdown_menu_pedido.get()
        if not menu_seleccionado:
            messagebox.showerror("Error", "Selecciona un menú para agregar al pedido.")
            return

        for menu in self.menus:
            if menu["nombre"] == menu_seleccionado:
                for item in self.pedidos:
                    if item["menu"] == menu_seleccionado:
                        item["cantidad"] += 1
                        self.actualizar_treeview_pedido()
                        return
                self.pedidos.append({"menu": menu_seleccionado, "cantidad": 1, "precio": 500})  # Precio fijo por ejemplo
                self.actualizar_treeview_pedido()
                return

    def actualizar_treeview_pedido(self):
        for item in self.treeview_pedido.get_children():
            self.treeview_pedido.delete(item)
        for pedido in self.pedidos:
            self.treeview_pedido.insert("", "end", values=(pedido["menu"], pedido["cantidad"], f"${pedido['cantidad'] * pedido['precio']}"))

    def generar_boleta(self):
        if not self.pedidos:
            messagebox.showerror("Error", "No hay pedidos para generar una boleta.")
            return
    
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Boleta de Pedido", ln=True, align="C")
        pdf.ln(10)  # Salto de línea

        # Información del cliente y pedido
        cliente = self.dropdown_cliente_pedido.get()
        pdf.cell(200, 10, txt=f"Cliente: {cliente}", ln=True)
        pdf.cell(200, 10, txt=f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    
        pdf.ln(10)

        total_pedido = 0
        for pedido in self.pedidos:
            pdf.cell(100, 10, txt=f"{pedido['menu']}", border=1)
            pdf.cell(50, 10, txt=str(pedido['cantidad']), border=1, align='C')
            pdf.cell(50, 10, txt=f"${pedido['precio'] * pedido['cantidad']}", border=1, align='R')
            pdf.ln(10)
            total_pedido += pedido['precio'] * pedido['cantidad']
    
        pdf.ln(10)
        pdf.cell(200, 10, txt=f"Total: ${total_pedido}", ln=True, align="R")
    
        # Guardar archivo PDF
        filename = f"boleta_{cliente}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Éxito", f"Boleta generada: {filename}")



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
