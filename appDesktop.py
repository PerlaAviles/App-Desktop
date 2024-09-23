import tkinter as tk
from tkinter import messagebox
import requests
import time
from datetime import datetime

# URL de MockAPI
API_URL = "https://66eb01ee55ad32cda47b4f5d.mockapi.io/IotCarStatus"


# Función para obtener la IP pública
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
        else:
            return "No IP Found"
    except Exception:
        return "Error Fetching IP"


# Función para obtener la fecha y hora actual en formato timestamp
def get_timestamp():
    return int(time.time())


# Función para obtener la fecha y hora actual en formato legible
def get_formatted_datetime():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


# Función para enviar los datos a la API
def send_data(status):
    name = entry_name.get()
    ip_client = ip_label.cget("text")
    date = get_timestamp()  # Obtener el timestamp actual

    if not name:
        messagebox.showwarning("Advertencia", "Por favor, ingrese su nombre.")
        return

    # Crear un diccionario con los datos
    data = {
        "name": name,
        "status": status,
        "date": date,
        "ipClient": ip_client
    }

    try:
        # Realizar una solicitud POST a la API
        response = requests.post(API_URL, json=data)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 201:
            messagebox.showinfo("Éxito", "Datos enviados correctamente.")
        else:
            messagebox.showerror("Error", f"Error al enviar los datos. Código: {response.status_code}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al enviar los datos: {str(e)}")


# Crear la ventana principal
root = tk.Tk()
root.title("Inyectar Registros a MockAPI")
root.geometry("400x300")
root.resizable(False, False)

# Etiquetas y campos de entrada
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True)

# Etiqueta y entrada para el nombre
tk.Label(frame, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
entry_name = tk.Entry(frame, width=30)
entry_name.grid(row=0, column=1, pady=5)

# Etiqueta para la IP
tk.Label(frame, text="IP del Cliente:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
default_ip = get_public_ip()
ip_label = tk.Label(frame, text=default_ip, font=("Arial", 12), width=30, anchor="w", relief="sunken", padx=5)
ip_label.grid(row=1, column=1, pady=5)

# Etiqueta para la fecha y hora actual
tk.Label(frame, text="Fecha y Hora Actual:", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
datetime_label = tk.Label(frame, text=get_formatted_datetime(), font=("Arial", 12), width=30, anchor="w",
                          relief="sunken", padx=5)
datetime_label.grid(row=2, column=1, pady=5)

# Etiqueta de selección de estado
tk.Label(frame, text="Seleccionar Status:", font=("Arial", 12)).grid(row=3, column=0, sticky="e", pady=10)

# Botones para seleccionar el estado
button_frame = tk.Frame(frame)
button_frame.grid(row=3, column=1, pady=10)

button_adelante = tk.Button(button_frame, text="Adelante", command=lambda: send_data("adelante"), width=10,
                            bg="#4CAF50", fg="white")
button_adelante.grid(row=0, column=1, padx=5)

button_atras = tk.Button(button_frame, text="Atrás", command=lambda: send_data("atrás"), width=10, bg="#FF5733",
                         fg="white")
button_atras.grid(row=1, column=1, padx=5, pady=5)

button_derecha = tk.Button(button_frame, text="Derecha", command=lambda: send_data("derecha"), width=10, bg="#3498DB",
                           fg="white")
button_derecha.grid(row=0, column=2, padx=5)

button_izquierda = tk.Button(button_frame, text="Izquierda", command=lambda: send_data("izquierda"), width=10,
                             bg="#F1C40F", fg="white")
button_izquierda.grid(row=1, column=2, padx=5, pady=5)

# Iniciar la aplicación
root.mainloop()
