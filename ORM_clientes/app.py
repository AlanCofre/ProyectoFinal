import customtkinter as ctk
from tkinter import ttk

# Configuración de la ventana principal
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestión de Ingredientes y Pedidos")
        self.geometry("750x600")

        self.pedido_id_counter = 1  # Contador para IDs de pedidos
        self.menu_dict = {}  # Diccionario para llevar el conteo de menús agregados

        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestañas
        self.tab_ingredientes = self.tabview.add("Ingredientes")
        self.crear_formulario_ingrediente(self.tab_ingredientes)

        self.tab_menu = self.tabview.add("Menú")
        self.crear_formulario_menu(self.tab_menu)

        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)

        self.tab_panel_compra = self.tabview.add("Panel de Compra")
        self.crear_formulario_panel_compra(self.tab_panel_compra)

        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedido(self.tab_pedidos)

        self.tab_graficos = self.tabview.add("Gráficos")
        self.crear_dropdown_graficos(self.tab_graficos)

    def crear_formulario_menu(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Campos de texto
        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_nombre_menu = ctk.CTkEntry(frame_superior)
        self.entry_nombre_menu.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10, sticky="w")
        self.entry_descripcion_menu = ctk.CTkEntry(frame_superior)
        self.entry_descripcion_menu.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # Botón alineado a la izquierda
        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=1, column=0, columnspan=4, pady=10, sticky="w")

        # Tabla
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Descripción"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre")
        self.treeview_menu.heading("Descripción", text="Descripción")
        self.treeview_menu.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_menu(self):
        nombre_menu = self.entry_nombre_menu.get()
        descripcion_menu = self.entry_descripcion_menu.get()
        if nombre_menu and descripcion_menu:
            self.treeview_menu.insert("", "end", values=(nombre_menu, descripcion_menu))
            self.dropdown_menu.configure(values=[menu[0] for menu in self.menu_dict.items()])
            print(f"Menú {nombre_menu} creado.")
        else:
            print("Error: Completa todos los campos para crear el menú.")

    def crear_formulario_panel_compra(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Menú").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.dropdown_menu = ctk.CTkComboBox(frame_superior, state="normal", values=[])
        self.dropdown_menu.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Botón alineado a la izquierda
        self.btn_agregar_compra = ctk.CTkButton(frame_superior, text="Agregar a la compra", command=self.agregar_a_compra)
        self.btn_agregar_compra.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="w")

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_compra = ttk.Treeview(frame_inferior, columns=("Menú", "Cantidad"), show="headings")
        self.treeview_compra.heading("Menú", text="Menú")
        self.treeview_compra.heading("Cantidad", text="Cantidad")
        self.treeview_compra.pack(pady=10, padx=10, fill="both", expand=True)

        self.btn_generar_boleta = ctk.CTkButton(parent, text="Generar Boleta", command=self.generar_boleta)
        self.btn_generar_boleta.pack(pady=10, padx=10)

    def agregar_a_compra(self):
        menu_seleccionado = self.dropdown_menu.get()
        if menu_seleccionado:
            if menu_seleccionado in self.menu_dict:
                self.menu_dict[menu_seleccionado] += 1
            else:
                self.menu_dict[menu_seleccionado] = 1
            self.actualizar_tabla_compra()

    def actualizar_tabla_compra(self):
        for item in self.treeview_compra.get_children():
            self.treeview_compra.delete(item)
        for menu, cantidad in self.menu_dict.items():
            self.treeview_compra.insert("", "end", values=(menu, cantidad))

    def generar_boleta(self):
        print("Boleta generada.")

    def crear_formulario_ingrediente(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame_superior)
        self.entry_nombre_ingrediente.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10, sticky="w")
        self.entry_tipo_ingrediente = ctk.CTkEntry(frame_superior)
        self.entry_tipo_ingrediente.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # Botón alineado a la izquierda
        self.btn_crear_ingrediente = ctk.CTkButton(frame_superior, text="Crear Ingrediente", command=self.crear_ingrediente)
        self.btn_crear_ingrediente.grid(row=1, column=0, columnspan=4, pady=10, sticky="w")

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_ingrediente(self):
        nombre_ingrediente = self.entry_nombre_ingrediente.get()
        tipo_ingrediente = self.entry_tipo_ingrediente.get()
        if nombre_ingrediente and tipo_ingrediente:
            self.treeview_ingredientes.insert("", "end", values=(nombre_ingrediente, tipo_ingrediente))
            print(f"Ingrediente {nombre_ingrediente} creado.")
        else:
            print("Error: Completa todos los campos para crear el ingrediente.")

    def crear_formulario_cliente(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10, sticky="w")
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10, sticky="w")

        # Botón alineado a la izquierda
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="w")

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Email"), show="headings")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if nombre and email:
            self.treeview_clientes.insert("", "end", values=(nombre, email))
            print(f"Cliente {nombre} creado.")
        else:
            print("Error: Completa todos los campos para crear el cliente.")

    def crear_formulario_pedido(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="ID Pedido").grid(row=0, column=0, pady=10, padx=10, sticky="w")
        self.entry_id_pedido = ctk.CTkEntry(frame_superior)
        self.entry_id_pedido.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Botón alineado a la izquierda
        self.btn_crear_pedido = ctk.CTkButton(frame_superior, text="Crear Pedido", command=self.crear_pedido)
        self.btn_crear_pedido.grid(row=1, column=0, columnspan=1, pady=10, padx=10, sticky="w")

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID Pedido", "Estado"), show="headings")
        self.treeview_pedidos.heading("ID Pedido", text="ID Pedido")
        self.treeview_pedidos.heading("Estado", text="Estado")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_pedido(self):
        id_pedido = self.entry_id_pedido.get()
        if id_pedido:
            self.treeview_pedidos.insert("", "end", values=(id_pedido, "Pendiente"))
            self.entry_id_pedido.delete(0, "end")
            print(f"Pedido {id_pedido} creado.")
        else:
            print("Error: Completa todos los campos para crear el pedido.")

    def crear_dropdown_graficos(self, parent):
        frame_graficos = ctk.CTkFrame(parent)
        frame_graficos.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_graficos, text="Selecciona un gráfico").grid(row=0, column=0, pady=10, padx=10)

        self.dropdown_graficos = ctk.CTkComboBox(frame_graficos, state="normal", values=["Opción 1", "Opción 2", "Opción 3"])
        self.dropdown_graficos.grid(row=0, column=1, pady=10, padx=10)

        # Botón alineado a la izquierda
        self.btn_seleccionar_grafico = ctk.CTkButton(frame_graficos, text="Seleccionar Gráfico", command=self.seleccionar_grafico)
        self.btn_seleccionar_grafico.grid(row=0, column=2, pady=10, sticky="w")

    def seleccionar_grafico(self):
        opcion_seleccionada = self.dropdown_graficos.get()
        print(f"Gráfico seleccionado: {opcion_seleccionada}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
