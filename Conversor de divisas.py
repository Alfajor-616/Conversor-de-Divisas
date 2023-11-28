import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from threading import Thread

# Obtener las monedas disponibles desde la API
response = requests.get(
    'https://free.currconv.com/api/v7/currencies?apiKey=98f5e93c8159297df987')
currencies = response.json()['results']
# se convierte a una lista las llaves obtenidas
currency_l = list(currencies.keys())
# se organiza la lista con el metodo sorted
currency_list = sorted([elemento for elemento in currency_l])

# Crear la ventana principal
root = tk.Tk()
# se le da el titulo a la ventana principal
root.title("Convertidor de Divisas")

# Crear ComboBox para la moneda de origen
label_origen = ttk.Label(root, text="Moneda de origen:")
label_origen.pack()
combo_origen = ttk.Combobox(root, values=currency_list)
combo_origen.pack()

# Crear ComboBox para la moneda de destino
label_destino = ttk.Label(root, text="Moneda de destino:")
label_destino.pack()
combo_destino = ttk.Combobox(root, values=currency_list)
combo_destino.pack()

# Crear función para realizar la conversión


def conversion():
    origen = combo_origen.get()
    destino = combo_destino.get()
    cantidad = float(entry_cantidad.get())
    url = f'https://free.currconv.com/api/v7/convert?q={origen}_{destino},{destino}_{origen}&compact=ultra&apiKey=98f5e93c8159297df987'
    response = requests.get(url)
    data = response.json()
    tasa_conversion = data[f'{origen}_{destino}']
    resultado = cantidad * tasa_conversion
    label_resultado.config(text=f"Resultado: {resultado} {destino}")


# Crear campos de entrada y botón para realizar la conversión
label_cantidad = ttk.Label(root, text="Cantidad a convertir:")
label_cantidad.pack()
entry_cantidad = ttk.Entry(root)
entry_cantidad.pack()
button_convertir = ttk.Button(root, text="Convertir", command=conversion)
button_convertir.pack()

# Crear el apartado de resultados
label_resultado = ttk.Label(root, text="Resultado:")
label_resultado.pack()

# Crear gráfica de fluctuación de la moneda
fig, ax = plt.subplots()
# Aquí puedes agregar los datos y configurar la gráfica según tus necesidades

# ax.plot(x_data, y_data)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()

# Función para realizar la solicitud HTTP en segundo plano


def get_currencies():
    global currencies
    response = requests.get(
        'https://free.currconv.com/api/v7/currencies?apiKey=98f5e93c8159297df987')
    currencies = response.json()['results']

# Función para realizar la conversión en segundo plano


def perform_conversion():
    Thread(target=get_currencies).start()
    Thread(target=conversion).start()


root.mainloop()
