import requests
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Obtener las monedas disponibles desde la API
response = requests.get(
    'https://free.currconv.com/api/v7/currencies?apiKey=98f5e93c8159297df987')
currencies = response.json()['results']
currency_l = list(currencies.keys())
currency_list = sorted([elemento for elemento in currency_l])

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Convertidor de Divisas")

# Crear ComboBox para la moneda de origen y destino
label_origen = ttk.Label(ventana, text="Moneda de origen:")
label_origen.pack()
combo_origen = ttk.Combobox(ventana, values=currency_list)
combo_origen.pack()

label_destino = ttk.Label(ventana, text="Moneda de destino:")
label_destino.pack()
combo_destino = ttk.Combobox(ventana, values=currency_list)
combo_destino.pack()

# Crear función para realizar la conversión
def conversion():
    origen = combo_origen.get()
    destino = combo_destino.get()
    cantidad = float(entry_cantidad.get())

    url = f'https://free.currconv.com/api/v7/convert?q={origen}_{destino}&compact=ultra&apiKey=98f5e93c8159297df987'
    response = requests.get(url)
    data = response.json()
    tasa_conversion = data[f'{origen}_{destino}']
    resultado = cantidad * tasa_conversion
    label_resultado.config(text=f"Resultado: {resultado} {destino}")

# Crear función para graficar
def graficar_en_front(origen, destino):
    url_fechas = f'https://free.currconv.com/api/v7/convert?q={origen}_{destino}&compact=ultra&date=2023-11-20&endDate=2023-11-28&apiKey=98f5e93c8159297df987'
    response_fechas = requests.get(url_fechas)
    data1 = response_fechas.json()

    fechas = list(data1[f'{origen}_{destino}'].keys())
    valores = list(data1[f'{origen}_{destino}'].values())

    fig, ax = plt.subplots()
    ax.plot(fechas, valores)
    ax.tick_params(axis='x', labelsize=6)
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor')
    ax.set_title(f'{origen}_{destino}')

    # Actualizar el área de dibujo
    global canvas
    if canvas is not None:
        canvas.get_tk_widget().pack_forget()
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.get_tk_widget().pack()
    canvas.draw()

# Inicializar canvas como None para la primera ejecución
canvas = None

# Crear campos de entrada y botón para la conversión
label_cantidad = ttk.Label(ventana, text="Cantidad a convertir:")
label_cantidad.pack()
entry_cantidad = ttk.Entry(ventana)
entry_cantidad.pack()
button_convertir = ttk.Button(ventana, text="Convertir", command=conversion)
button_convertir.pack()
label_resultado = ttk.Label(ventana, text="Resultado:")
label_resultado.pack()

button_graficar = ttk.Button(ventana, text="Mostrar Gráfico", command=lambda: graficar_en_front(combo_origen.get(), combo_destino.get()))
button_graficar.pack()

ventana.mainloop()
