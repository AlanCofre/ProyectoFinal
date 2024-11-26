import customtkinter as ctk
from tkinter import messagebox, ttk

# Datos locales en memoria
clientes = []
pedidos = []

# Configuración de la ventana principal
ctk.set_appearance_mode("System")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("dark-blue")  # Opciones: "blue", "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self): 
        super().__init__()

        self.title("Gestión de Clientes y Pedidos")
        self.geometry("750x600")

        # Crear el Tabview (pestañas)
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=20, padx=20, fill="both", expand=True)

        # Pestaña de Clientes
        self.tab_clientes = self.tabview.add("Clientes")
        self.crear_formulario_cliente(self.tab_clientes)

        # Pestaña de Pedidos
        self.tab_pedidos = self.tabview.add("Pedidos")
        self.crear_formulario_pedido(self.tab_pedidos)

        # Revisar el cambio de pestaña periódicamente
        self.current_tab = self.tabview.get()  # Almacena la pestaña actual
        self.after(500, self.check_tab_change)  # Llama a check_tab_change cada 500 ms

    def check_tab_change(self):
        """Revisa si la pestaña activa cambió a 'Pedidos'."""
        new_tab = self.tabview.get()
        if new_tab != self.current_tab:
            self.current_tab = new_tab
            if new_tab == "Pedidos":
                self.actualizar_emails_combobox()
        self.after(500, self.check_tab_change)  # Vuelve a revisar cada 500 ms

    def crear_formulario_cliente(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de clientes."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Nombre").grid(row=0, column=0, pady=10, padx=10)
        self.entry_nombre = ctk.CTkEntry(frame_superior)
        self.entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        ctk.CTkLabel(frame_superior, text="Email").grid(row=0, column=2, pady=10, padx=10)
        self.entry_email = ctk.CTkEntry(frame_superior)
        self.entry_email.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_cliente = ctk.CTkButton(frame_superior, text="Crear Cliente", command=self.crear_cliente)
        self.btn_crear_cliente.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_cliente = ctk.CTkButton(frame_superior, text="Actualizar Cliente", command=self.actualizar_cliente)
        self.btn_actualizar_cliente.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_cliente = ctk.CTkButton(frame_superior, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.btn_eliminar_cliente.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los clientes
        self.treeview_clientes = ttk.Treeview(frame_inferior, columns=("Email", "Nombre"), show="headings")
        self.treeview_clientes.heading("Email", text="Email")
        self.treeview_clientes.heading("Nombre", text="Nombre")
        self.treeview_clientes.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_clientes()

    def crear_formulario_pedido(self, parent):
        """Crea el formulario en el Frame superior y el Treeview en el Frame inferior para la gestión de pedidos."""
        # Frame superior para el formulario y botones
        frame_superior = ctk.CTkFrame(parent)
        frame_superior.pack(pady=10, padx=10, fill="x")

        ctk.CTkLabel(frame_superior, text="Cliente Email").grid(row=0, column=0, pady=10, padx=10)
        
        # Combobox para seleccionar el email del cliente
        self.combobox_cliente_email = ttk.Combobox(frame_superior, state="readonly")
        self.combobox_cliente_email.grid(row=0, column=1, pady=10, padx=10)
        self.actualizar_emails_combobox()  # Llenar el combobox con emails de los clientes

        ctk.CTkLabel(frame_superior, text="Descripción").grid(row=0, column=2, pady=10, padx=10)
        self.entry_descripcion = ctk.CTkEntry(frame_superior)
        self.entry_descripcion.grid(row=0, column=3, pady=10, padx=10)

        # Botones alineados horizontalmente en el frame superior
        self.btn_crear_pedido = ctk.CTkButton(frame_superior, text="Crear Pedido", command=self.crear_pedido)
        self.btn_crear_pedido.grid(row=1, column=0, pady=10, padx=10)

        self.btn_actualizar_pedido = ctk.CTkButton(frame_superior, text="Actualizar Pedido", command=self.actualizar_pedido)
        self.btn_actualizar_pedido.grid(row=1, column=1, pady=10, padx=10)

        self.btn_eliminar_pedido = ctk.CTkButton(frame_superior, text="Eliminar Pedido", command=self.eliminar_pedido)
        self.btn_eliminar_pedido.grid(row=1, column=2, pady=10, padx=10)

        # Frame inferior para el Treeview
        frame_inferior = ctk.CTkFrame(parent)
        frame_inferior.pack(pady=10, padx=10, fill="both", expand=True)

        # Treeview para mostrar los pedidos
        self.treeview_pedidos = ttk.Treeview(frame_inferior, columns=("ID", "Cliente Email", "Descripción"), show="headings")
        self.treeview_pedidos.heading("ID", text="ID")
        self.treeview_pedidos.heading("Cliente Email", text="Cliente Email")
        self.treeview_pedidos.heading("Descripción", text="Descripción")
        self.treeview_pedidos.pack(pady=10, padx=10, fill="both", expand=True)

        self.cargar_pedidos()

    # Método para actualizar los correos electrónicos en el Combobox
    def actualizar_emails_combobox(self):
        """Llena el Combobox con los emails de los clientes."""
        emails = [cliente["email"] for cliente in clientes]
        self.combobox_cliente_email['values'] = emails

    # Métodos CRUD para Clientes
    def cargar_clientes(self):
        self.treeview_clientes.delete(*self.treeview_clientes.get_children())
        for cliente in clientes:
            self.treeview_clientes.insert("", "end", values=(cliente["email"], cliente["nombre"]))

    def crear_cliente(self):
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if nombre and email:
            if any(cliente["email"] == email for cliente in clientes):
                messagebox.showwarning("Error", "El cliente ya existe.")
            else:
                clientes.append({"nombre": nombre, "email": email})
                messagebox.showinfo("Éxito", "Cliente creado correctamente.")
                self.cargar_clientes()
                self.actualizar_emails_combobox()  # Actualizar el Combobox con el nuevo email
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un cliente.")
            return
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        if not nombre.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un nombre.")
            return
        if not email.strip():
            messagebox.showwarning("Campo Vacío", "Por favor, ingrese un email.")
            return
        email_viejo = self.treeview_clientes.item(selected_item)["values"][0]
        for cliente in clientes:
            if cliente["email"] == email_viejo:
                cliente["nombre"] = nombre
                cliente["email"] = email
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
                self.cargar_clientes()
                break

    def eliminar_cliente(self):
        selected_item = self.treeview_clientes.selection()
        if selected_item:
            email = self.treeview_clientes.item(selected_item)["values"][0]
            clientes[:] = [cliente for cliente in clientes if cliente["email"] != email]
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            self.cargar_clientes()

    # Métodos CRUD para Pedidos
    def cargar_pedidos(self):
        self.treeview_pedidos.delete(*self.treeview_pedidos.get_children())
        for pedido in pedidos:
            self.treeview_pedidos.insert("", "end", values=(pedido["id"], pedido["cliente_email"], pedido["descripcion"]))

    def crear_pedido(self):
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            id_pedido = len(pedidos) + 1
            pedidos.append({"id": id_pedido, "cliente_email": cliente_email, "descripcion": descripcion})
            messagebox.showinfo("Éxito", "Pedido creado correctamente.")
            self.cargar_pedidos()
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def actualizar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor, seleccione un pedido.")
            return
        cliente_email = self.combobox_cliente_email.get()
        descripcion = self.entry_descripcion.get()
        if cliente_email and descripcion:
            id_pedido = self.treeview_pedidos.item(selected_item)["values"][0]
            for pedido in pedidos:
                if pedido["id"] == id_pedido:
                    pedido["cliente_email"] = cliente_email
                    pedido["descripcion"] = descripcion
                    messagebox.showinfo("Éxito", "Pedido actualizado correctamente.")
                    self.cargar_pedidos()
                    break
        else:
            messagebox.showwarning("Campos Vacíos", "Por favor, ingrese todos los campos.")

    def eliminar_pedido(self):
        selected_item = self.treeview_pedidos.selection()
        if selected_item:
            id_pedido = self.treeview_pedidos.item(selected_item)["values"][0]
            pedidos[:] = [pedido for pedido in pedidos if pedido["id"] != id_pedido]
            messagebox.showinfo("Éxito", "Pedido eliminado correctamente.")
            self.cargar_pedidos()

# Crear y ejecutar la aplicación
if __name__ == "__main__":
    app = App()
    app.mainloop()
