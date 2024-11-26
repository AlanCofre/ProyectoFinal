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

        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedido(self.tab_pedidos)

        self.tab_graficos = self.tabview.add("Gráficos")
        self.crear_dropdown_graficos(self.tab_graficos)  # Llamada para crear el dropdown en "Gráficos"

    def crear_formulario_menu(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre del Menú").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_menu = ctk.CTkEntry(frame_superior)
        self.entry_nombre_menu.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_descripcion_menu = ctk.CTkEntry(frame_superior)
        self.entry_descripcion_menu.grid(row=0, column=3, pady=10, padx=10)

        self.btn_crear_menu = ctk.CTkButton(frame_superior, text="Crear Menú", command=self.crear_menu)
        self.btn_crear_menu.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_menu = ttk.Treeview(frame_inferior, columns=("Nombre", "Descripción"), show="headings")
        self.treeview_menu.heading("Nombre", text="Nombre")
        self.treeview_menu.heading("Descripción", text="Descripción")
        self.treeview_menu.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_formulario_ingrediente(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre_ingrediente = ctk.CTkEntry(frame_superior)
        self.entry_nombre_ingrediente.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Tipo").grid(row=0, column=2, pady=10, padx=10)
        self.entry_tipo_ingrediente = ctk.CTkEntry(frame_superior)
        self.entry_tipo_ingrediente.grid(row=0, column=3, pady=10, padx=10)

        self.btn_crear_ingrediente = ctk.CTkButton(frame_superior, text="Crear Ingrediente", command=self.crear_ingrediente)
        self.btn_crear_ingrediente.grid(row=1, column=0, pady=10, padx=10)

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_ingredientes = ttk.Treeview(frame_inferior, columns=("Nombre", "Tipo"), show="headings")
        self.treeview_ingredientes.heading("Nombre", text="Nombre")
        self.treeview_ingredientes.heading("Tipo", text="Tipo")
        self.treeview_ingredientes.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_formulario_cliente(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Email", "Nombre"), show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_formulario_pedido(self, parent):
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Cliente Email").grid(row=0, column=0, pady=10, padx=10)
        self.combobox_cliente_email = ctk.CTkComboBox(frame_superior, state="readonly", values=[])
        self.combobox_cliente_email.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_descripcion.grid(row=0, column=3, pady=10, padx=10)

        self.btn_crear_pedido = ctk.CTkButton(frame_superior, text="Crear Pedido", command=self.crear_pedido)
        self.btn_crear_pedido.grid(row=1, column=0, pady=10, padx=10)

        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID", "Cliente", "Descripción"), show="headings")
        self.treeview_pedidos.heading("ID", text="ID")
        self.treeview_pedidos.heading("Cliente", text="Cliente")
        self.treeview_pedidos.heading("Descripción", text="Descripción")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if nombre and email:
            self.treeview_clientes.insert("", "end", values=(email, nombre))
            print(f"Cliente {nombre} con email {email} creado.")
            self.actualizar_combobox()
        else:
            print("Error: Completa todos los campos para crear el cliente.")

    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            self.treeview_pedidos.insert("", "end", values=(self.pedido_id_counter, cliente_email, descripcion))
            print(f"Pedido creado para {cliente_email}: {descripcion}")
            self.pedido_id_counter += 1
        else:
            print("Error: Completa todos los campos para crear el pedido.")

    def crear_menu(self):
        nombre_menu = self.entry_nombre_menu.get()
        descripcion_menu = self.entry_descripcion_menu.get()
        if nombre_menu and descripcion_menu:
            self.treeview_menu.insert("", "end", values=(nombre_menu, descripcion_menu))
            print(f"Menú {nombre_menu} creado.")
        else:
            print("Error: Completa todos los campos para crear el menú.")

    def crear_ingrediente(self):
        nombre_ingrediente = self.entry_nombre_ingrediente.get()
        tipo_ingrediente = self.entry_tipo_ingrediente.get()
        if nombre_ingrediente and tipo_ingrediente:
            self.treeview_ingredientes.insert("", "end", values=(nombre_ingrediente, tipo_ingrediente))
            print(f"Ingrediente {nombre_ingrediente} creado.")
        else:
            print("Error: Completa todos los campos para crear el ingrediente.")

    def actualizar_combobox(self):
        self.combobox_cliente_email.set('')
        self.combobox_cliente_email.set([item[0] for item in self.treeview_clientes.get_children()])

    def crear_dropdown_graficos(self, parent):
        # Frame superior
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        # Crear el Label para el dropdown
        label = ctk.CTkLabel(frame_superior, text="Elige el gráfico", anchor="center")
        label.grid(row=0, column=0, pady=10, padx=10)

        # Crear el dropdown con opciones
        opciones = ["Gráfico de Ventas", "Gráfico de Ingredientes", "Gráfico de Clientes"]
        dropdown = ctk.CTkComboBox(frame_superior, values=opciones, state="normal")
        dropdown.grid(row=1, column=0, pady=10, padx=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()
