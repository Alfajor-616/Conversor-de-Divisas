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
# Se convierte a una lista las llaves obtenidas
currency_l = list(currencies.keys())
# Se organiza la lista con el metodo sorted
currency_list = sorted([elemento for elemento in currency_l])

# Crear la ventana principal
ventana = tk.Tk()
# se le da el titulo a la ventana principal
ventana.title("Convertidor de Divisas")

# Crear ComboBox para la moneda de origen
label_origen = ttk.Label(ventana, text="Moneda de origen:")
label_origen.pack()
combo_origen = ttk.Combobox(ventana, values=currency_list)
combo_origen.pack()

# Crear ComboBox para la moneda de destino
label_destino = ttk.Label(ventana, text="Moneda de destino:")
label_destino.pack()
combo_destino = ttk.Combobox(ventana, values=currency_list)
combo_destino.pack()

# Crear funciónes para realizar la conversión y la grafica


def conversion():
    # Extraer datos de los widgets de la interfaz gráfica
    origen = combo_origen.get()
    destino = combo_destino.get()
    cantidad = float(entry_cantidad.get())

    # Enviar solicitud a la API
    url = f'https://free.currconv.com/api/v7/convert?q={origen}_{destino},{destino}_{origen}&compact=ultra&apiKey=98f5e93c8159297df987'

    response = requests.get(url)
    data = response.json()
    # Recuperar la tasa de conversión
    tasa_conversion = data[f'{origen}_{destino}']
    # Calcular el resultado
    resultado = cantidad * tasa_conversion
    # Actualizar la etiqueta con el resultado
    label_resultado.config(text=f"Resultado: {resultado} {destino}")


def graficar_en_front(origen, destino):

    url_fechas = f'https://free.currconv.com/api/v7/convert?q={origen}_{destino},{destino}_{origen}&compact=ultra&date=2023-11-20&endDate=2023-11-28&apiKey=98f5e93c8159297df987'

    # Obtener datos desde la URL
    response_fechas = requests.get(url_fechas)
    data1 = response_fechas.json()

    # Extraer fechas y valores de los datos
    fechas = list(data1[f'{origen}_{destino}'].keys())
    valores = list(data1[f'{origen}_{destino}'].values())

    # Crear un gráfico con fechas en el eje x y valores en el eje y
    fig, ax = plt.subplots()
    ax.plot(fechas, valores)

    # Configurar las etiquetas del eje x del gráfico
    ax.tick_params(axis='x', labelsize=6)

    # Establecer etiquetas y título para el gráfico
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Valor')
    ax.set_title(f'{origen}_{destino}')

    # Mostrar el gráfico en la interfaz gráfica
    canvas = FigureCanvasTkAgg(fig, master=ventana)
    canvas.get_tk_widget().pack()
    canvas.draw()
    canvas.flush_events()


# Crear campos de entrada y botón para realizar la conversión y crear boton para mostrar el grafico
label_cantidad = ttk.Label(ventana, text="Cantidad a convertir:")
label_cantidad.pack()
entry_cantidad = ttk.Entry(ventana)
entry_cantidad.pack()
button_convertir = ttk.Button(ventana, text="Convertir", command=conversion)
button_convertir.pack()
label_resultado = ttk.Label(ventana, text="Resultado:")
label_resultado.pack()
button_graficar = ttk.Button(ventana, text="Mostrar Gráfico", command=lambda: graficar_en_front(
    combo_origen.get(), combo_destino.get()))
button_graficar.pack()

ventana.mainloop()
