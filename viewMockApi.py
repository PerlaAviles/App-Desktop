import tkinter as tk
from tkinter import ttk, messagebox
import requests

# URL de MockAPI
API_URL = "https://66eb01ee55ad32cda47b4f5d.mockapi.io/IotCarStatus"

# Función para obtener los últimos 10 registros de MockAPI ordenados por ID (descendente)
def fetch_latest_records():
    try:
        response = requests.get(API_URL + "?sortBy=id&order=desc&limit=10")
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            messagebox.showerror("Error", f"Error al obtener los datos. Código: {response.status_code}")
            return []
    except Exception as e:
        messagebox.showerror("Error", f"Error al conectarse a MockAPI: {str(e)}")
        return []

# Función para cargar los datos en la tabla
def load_data():
    records = fetch_latest_records()

    # Limpiar la tabla antes de cargar nuevos datos
    for row in table.get_children():
        table.delete(row)

    # Ordenar los registros por ID en orden descendente
    records.sort(key=lambda x: int(x['id']), reverse=True)

    # Insertar los registros en la tabla
    for record in records[:10]:  # Mostrar solo hasta 10 registros
        table.insert("", "end",
                     values=(record['id'], record['name'], record['status'], record['date'], record['ipClient']))

# Crear la ventana principal
root = tk.Tk()
root.title("Últimos 10 Registros - MockAPI")
root.geometry("700x400")
root.resizable(False, False)

# Estilo de la tabla
style = ttk.Style()
style.configure("Treeview.Heading", font=("Arial", 10, "bold"), foreground="blue")
style.configure("Treeview", rowheight=25, font=("Arial", 9))

# Crear la tabla
columns = ("ID", "Nombre", "Status", "Fecha (Timestamp)", "IP del Cliente")
table = ttk.Treeview(root, columns=columns, show="headings")

# Definir encabezados de la tabla y ajustar el ancho de las columnas
table.heading("ID", text="ID")
table.heading("Nombre", text="Nombre")
table.heading("Status", text="Status")
table.heading("Fecha (Timestamp)", text="Fecha (Timestamp)")
table.heading("IP del Cliente", text="IP del Cliente")

table.column("ID", width=50, anchor="center")
table.column("Nombre", width=150, anchor="center")
table.column("Status", width=100, anchor="center")
table.column("Fecha (Timestamp)", width=150, anchor="center")
table.column("IP del Cliente", width=150, anchor="center")

# Estilo de barras de desplazamiento (scrollbar)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

table.pack(expand=True, fill="both", padx=10, pady=10)

# Botón para refrescar los datos
refresh_button = tk.Button(root, text="Refrescar", command=load_data, font=("Arial", 10, "bold"), bg="lightblue",
                           fg="black")
refresh_button.pack(pady=10)

# Cargar los datos al iniciar la aplicación
load_data()

# Iniciar la aplicación
root.mainloop()

