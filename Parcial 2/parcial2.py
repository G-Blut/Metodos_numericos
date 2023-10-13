import tkinter as tk
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import random

from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#from reportlab.lib.pagesizes import letter
#from reportlab.pdfgen import canvas

# Función para validar y ejecutar el método seleccionado
def Validacion():
    seleccion = metodo_seleccionado.get()
    if seleccion == 1:
        MetodoTanteo()
    elif seleccion == 2:
        MetodoBiseccion()
    elif seleccion == 3:
        MetodoReglaFalsa()
    elif seleccion == 4:  # Agregado el método de la secante
        MetodoSecante()
    

# Función para evaluar la ecuación
def pol(x):
    ecuacion = entrada_ecuacion.get()
    try:
        simbolo = sp.symbols('x')
        simbolo_ecuacion = sp.sympify(ecuacion)
        resultado = simbolo_ecuacion.subs(simbolo, x)
        return resultado
    except Exception as e:
        return None

# Función para generar puntos de arranque
def GeneradorPuntosArranque():
    while True:
        Xa = -1000 * random.random()
        Xb = -Xa
        if pol(Xa) * pol(Xb) < 0:
            break
    mensaje_puntos_arranque.set(f"xa={Xa}, xb={Xb}")

# Función para el método de Tanteo
def MetodoTanteo():
    X_0 = random.randint(-100, 100)
    precision = float(entrada_precision.get()) if entrada_precision.get() else 0.001
    resultado = None

    for i in range(100000):
        if abs(pol(X_0)) <= precision:
            resultado = f"La solución es: {X_0} en {i} iteraciones"
            break
        else:
            if pol(X_0) > 0:
                X_0 = X_0 - 0.5
            else:
                X_0 = X_0 + 0.5

    mensaje_resultado.set(resultado)
    Graficador(-10, 10, X_0)

# Función para el método de Bisección
def MetodoBiseccion():
    while True:
        Xa = -1000 * random.random()
        Xb = -Xa
        Xc = (Xa + Xb) / 2
        if pol(Xa) * pol(Xb) < 0:
            break

    precision = float(entrada_precision.get()) if entrada_precision.get() else 0.001

    cont = 0
    while True:
        cont += 1
        if abs(pol(Xc)) <= precision:
            break
        elif pol(Xa) * pol(Xc) < 0:
            Xb = Xc
            Xc = (Xa + Xb) / 2
        else:
            Xa = Xc
            Xc = (Xa + Xb) / 2

    mensaje_resultado.set(f"La solución es: {Xc} encontrada en {cont} iteraciones, xa={Xa}, xb={Xb}")
    Graficador(Xa, Xb, Xc)

# Función para el método de Regla Falsa
def MetodoReglaFalsa():
    while True:
        Xa = -1000 * random.random()
        Xb = -Xa
        Xc = (Xa - (pol(Xa) * (Xb - Xa)) / (pol(Xb) - pol(Xa)))
        if pol(Xa) * pol(Xb) < 0:
            break

    precision = float(entrada_precision.get()) if entrada_precision.get() else 0.001

    cont = 0
    while True:
        cont += 1
        if abs(pol(Xc)) <= precision:
            break
        elif pol(Xa) * pol(Xc) < 0:
            Xb = Xc
            Xc = (Xa - (pol(Xa) * (Xb - Xa)) / (pol(Xb) - pol(Xa)))
        else:
            Xa = Xc
            Xc = (Xa - (pol(Xa) * (Xb - Xa)) / (pol(Xb) - pol(Xa)))

    mensaje_resultado.set(f"La solución es: {Xc} encontrada en {cont} iteraciones, xa={Xa}, xb={Xb}")
    Graficador(Xa, Xb, Xc)
    
# Función para el método de la Secante
def MetodoSecante():
    Xb = random.uniform(1, 50)
    Xa = Xb - 0.1
    precision = float(entrada_precision.get()) if entrada_precision.get() else 0.00001
    mensaje_puntos_arranque.set(f"xa={Xa}, xb={Xb}")

    cont = 0

    while True:
        cont += 1
        f_Xa = (pol(Xa) - pol(Xb)) / (Xa - Xb)
        Xc = Xa - (pol(Xa) / f_Xa)

        if abs(pol(Xc)) <= precision:
            break

        if pol(Xc) > 0:
            Xa = Xc
        else:
            Xb = Xc

    mensaje_resultado.set(f"La solución es: {round(Xc, 3)} encontrada en {cont} iteraciones")
    Graficador(Xa, Xb, Xc)


def MostrarAyuda():
    ventana_ayuda = tk.Toplevel(app)
    ventana_ayuda.title("Ayuda")
    
    texto_ayuda = tk.Label(ventana_ayuda, text="Bienvenido a la Calculadora de Ecuaciones"
                           "\n"
                           "\n"
                           "Sobre el programa y su uso :"
                           "\n"
                           "\n"
                           "1. Ingrese la ecuacion a resolver en el campo: 'Ingrese la ecuación'.\n"
                           "2. Seleccione el método que desea utilizar.\n"
                           "3. Cuenta con la opcion de ajustar la precision del programa, ingrese la precisión deseada.\n"
                           "4. Debe hacer click en el boton 'CALCULAR' para iniciar la ejecucion del programa.\n"
                           "5. Puede generar un reporte con los resultados en un archivo PDF haciendo click en 'GUARDAR PDF'.\n"
                           "6. Para salir del programa, simplemente cierre la ventana principal.\n"
                           "\n¡Muchas gracias por utilizar este programa espero disfrute de la experiencia!", justify="left")
    
    texto_ayuda.pack(padx=20, pady=20)

# Crear la ventana principal
app = tk.Tk()
app.title("Calculadora de Ecuaciones")
app.configure(bg="lightblue")

# Crear marcos
MarcoIngresoDatos = ttk.Frame(app)
MarcoIngresoDatos.pack(pady=10, padx=10)

MarcoSalidaDatos = ttk.Frame(app)
MarcoSalidaDatos.pack(pady=10, padx=10)

# Crear entrada de ecuación
ttk.Label(MarcoIngresoDatos, text="Ingrese la ecuación:").grid(row=0, column=0, padx=10, pady=5)
entrada_ecuacion = ttk.Entry(MarcoIngresoDatos, width=40)
entrada_ecuacion.grid(row=0, column=1, padx=10, pady=5)

# Crear radio buttons
metodo_seleccionado = tk.IntVar()
metodo_seleccionado.set(1)

ttk.Label(MarcoIngresoDatos, text="Seleccione el método a utilizar:").grid(row=1, column=0, padx=10, pady=5)

ttk.Radiobutton(MarcoIngresoDatos, text="Tanteo", variable=metodo_seleccionado, value=1).grid(row=1, column=1, padx=10, pady=5)
ttk.Radiobutton(MarcoIngresoDatos, text="Bisección", variable=metodo_seleccionado, value=2).grid(row=1, column=2, padx=10, pady=5)
ttk.Radiobutton(MarcoIngresoDatos, text="Regla Falsa", variable=metodo_seleccionado, value=3).grid(row=1, column=3, padx=10, pady=5)
ttk.Radiobutton(MarcoIngresoDatos, text="Secante",  variable=metodo_seleccionado, value=4).grid(row=1, column=4, padx=10, pady=5)

# Crear entrada para la precisión deseada
ttk.Label(MarcoIngresoDatos, text="Precisión deseada: (0.01, 0.001,...)").grid(row=3, column=0, padx=10, pady=5)
entrada_precision = ttk.Entry(MarcoIngresoDatos, width=10)
entrada_precision.grid(row=3, column=1, padx=10, pady=5)

# Botón para calcular
ttk.Button(MarcoIngresoDatos, text="Calcular", command=Validacion).grid(row=4, column=1, padx=10, pady=10)

# Botón para la ayuda
ttk.Button(MarcoIngresoDatos, text="Ayuda", command=MostrarAyuda).grid(row=4, column=2, padx=10, pady=10)

# Crear marco para mostrar resultados
mensaje_puntos_arranque = tk.StringVar()
mensaje_resultado = tk.StringVar()

ttk.Label(MarcoSalidaDatos, textvariable=mensaje_puntos_arranque).pack(padx=10, pady=5)
ttk.Label(MarcoSalidaDatos, textvariable=mensaje_resultado).pack(padx=10, pady=5)

# Crear el gráfico
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=MarcoSalidaDatos)
canvas.get_tk_widget().pack(padx=10, pady=10)

# Función para graficar
def Graficador(Xa, Xb, Xc):
    if isinstance(Xa, (int, float)) and isinstance(Xb, (int, float)) and isinstance(Xc, (int, float)):
        X = np.linspace(Xa - 1, Xb + 1, 10000).astype(float)
        Y = [pol(x) for x in X]

        ax.clear()
        ax.plot(X, Y, '-y')

        plt.axhline(0, color='red', linewidth=1.8)
        plt.axvline(0, color='red', linewidth=1.8)

        ax.plot([Xa, Xb], [pol(Xa), pol(Xb)], 'g')
        ax.plot(Xc, pol(Xc), 'ok')

        ax.grid()
        ax.set_xlabel('Valores de x')
        ax.set_ylabel('Valores de y')

        canvas.draw()
    else:
        print("Valores no validos para Xa, Xb o Xc.")


# Ejecutar la aplicación
app.mainloop()
