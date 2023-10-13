import tkinter as tk
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Crear form contenedor del proyecto
app = tk.Tk()
app.title("Parcial 1 - Calculadora de Ecuaciones")
app.config(bg="blue")

#Crear el contenedor donde se "ingresan los datos y seleccionan opciones"
MarcoIngresoDatos = Frame()
MarcoIngresoDatos.pack()
MarcoIngresoDatos.config(width="800", height="800",bg="red")

#Crear el contenedor donde se muestran los outputs
MarcoSalidaDatos = Frame()
MarcoSalidaDatos.pack()
MarcoSalidaDatos.config(width="800", height="800",bg="black")

# Campo de entrada de la ecuación
labelEcuacion = ttk.Label(MarcoIngresoDatos, text="Ingrese la ecuación:", width=40)
labelEcuacion.pack()
IngresoEcuacion = ttk.Entry(MarcoIngresoDatos, width=40)
IngresoEcuacion.pack()

#Creacion del modelo de seleccion de proceso
def Proceso():
    if seleccion.get()==1:
        mensaje="Has seleccionado el metodo de Tanteo"
        MetodoTanteo()
    elif seleccion.get()==2:
        mensaje="Has seleccionado el metodo de Biseccion"
        MetodoBiseccion()
    elif seleccion.get()==3:
        mensaje="Has seleccionado el metodo de Regla Falsa"
        MetodoReglaFalsa()
    lblMensaje.config(text=mensaje)

seleccion= tk.IntVar(value=0)

#Creacion de Radio Buttons
rbnTanteo = tk.Radiobutton(MarcoIngresoDatos, text="Tanteo", variable=seleccion, value=1)
rbnTanteo.pack()
rbnBiseccion = tk.Radiobutton(MarcoIngresoDatos, text="Biseccion", variable=seleccion, value=2)
rbnBiseccion.pack()
rbnReglaFalsa = tk.Radiobutton(MarcoIngresoDatos, text="Regla Falsa", variable=seleccion, value=3)
rbnReglaFalsa.pack()

lblMensaje = tk.Label(MarcoSalidaDatos, width=50)
lblMensaje.pack()
lblMensaje1 = tk.Label(MarcoSalidaDatos, width=105)
lblMensaje1.pack()

fig, ax = plt.subplots(figsize=(6,4))

# Crear el widget de canvas de Tkinter para la figura
canvas = FigureCanvasTkAgg(fig, master=MarcoSalidaDatos)
canvas.get_tk_widget().pack()

#Metodo para el control de disparo
def Validacion():
    Proceso()

#Creacion del boton de validacion
boton = ttk.Button(MarcoIngresoDatos, text= "Solucionar", command=Validacion)
boton.pack()

#Función para evaluar la ecuación según el método seleccionado
def pol(x):
    ecuacion = IngresoEcuacion.get()
    try:
        simbolo = sp.symbols('x')
        simboloEcuacion = sp.sympify(ecuacion)
        resultado = simboloEcuacion.subs(simbolo, x)
        return resultado
    except Exception as e:
        return None

#def pol(x):
    #return (x**4-10*x**3+35*x**2-50*x+24)
#x**2 - 5*x  + 6
#x**3-6*x**2+11*x-6
#x**4-10*x**3+35*x**2-50*x+24

#Generador de puntos de arranque
def GeneradorPuntosArranque():
    from random import random
    while True:
      Xa=-1000*random();Xb=-Xa
      if pol(Xa) * pol(Xb)<0:
        break
    lblMensaje1.config(text=f"xa={Xa} xb= {Xb}")
    return Xa, Xb

#Metodo de Tanteo con el codigo de ejecucion
def MetodoTanteo():
    import random as rnd
    X_0 = rnd.randint(-100,100)

    for i in range(100000):
      if abs(pol(X_0))<=0.001:
        print(X_0)
        print(i,' iteraciones')
        break
      else:
        if pol(X_0)>0:
          X_0 = X_0 - 0.5
        else:
          X_0 = X_0 + 0.5
    lblMensaje1.config(text=f"La solucion es: {X_0} en {i} iteraciones")
#-----------------------------------------

#Metodo de biseccion con el codigo de ejecucion
def MetodoBiseccion():
    #Método de bisección
    from random import random
    while True:
      Xa=-1000*random();Xb=-Xa;Xc=(Xa+Xb)/2
      if pol(Xa)*pol(Xb)<0:
        break

    cont=0
    while True:
      cont+=1
      if abs(pol(Xc))<=0.001:
        break
      elif pol(Xa)*pol(Xc)<0:
        Xb=Xc;Xc=(Xa+Xb)/2
      else:
        Xa=Xc;Xc=(Xa+Xb)/2
        
    print('Xa: ',Xa,' Xb: ',Xb,' Xc: ',Xc)
    print(cont,' iteraciones')
    lblMensaje1.config(text=f"La solucion es: {Xc} encontrada en {cont} iteraciones, xa={Xa} xb= {Xb}")
    Graficador(Xa, Xb, Xc)
#-----------------------------------------

#Metodo de Regla Falsa con el codigo de ejecucion
def MetodoReglaFalsa():
    from random import random
    while True:
      Xa=-1000*random(); Xb=-Xa; Xc=(Xa-((pol(Xa)*(Xb-Xa))/(pol(Xb)-pol (Xa))))
      if pol(Xa)*pol(Xb)<0:
        break
    cont=0
    while True:
      cont+=1
      if abs(pol(Xc))<=0.001:
        break
      elif pol(Xa)*pol(Xc)<0:
        Xb=Xc; Xc=(Xa-((pol(Xa)*(Xb-Xa))/(pol(Xb)-pol(Xa))))
      else:
        Xa=Xc; Xc=(Xa-((pol(Xa)*(Xb-Xa))/(pol(Xb)-pol(Xa))))
        
    print('Xa: ',Xa,' Xb: ',Xb,' Xc: ',Xc)
    print(cont,' iteraciones')
    lblMensaje1.config(text=f"La  regla solucion es: {Xc} encontrada en {cont} iteraciones, xa={Xa} xb= {Xb}")
    Graficador(Xa, Xb, Xc)
    
#-----------------------------------------
def Graficador(Xa, Xb, Xc):
    
    X = np.linspace(Xa - 1, Xb + 1, 10000).astype(float)
    Y = [pol(x) for x in X]

    # Borrar el gráfico anterior
    ax.clear()

    # Dibujar la función
    ax.plot(X, Y, '-y')

    plt.axhline(0, color='red',linewidth=1.8)
    plt.axvline(0, color='red',linewidth=1.8)

    # Dibujar los puntos
    ax.plot([Xa, Xb], [pol(Xa), pol(Xb)],'g',)
    ax.plot(Xc, pol(Xc), 'ok')
    
    ax.grid()
    ax.set_xlabel('Valores de x')
    ax.set_ylabel('Valores de y')
    
    plt.text(1.5,30,"",fontsize=14)

    # Actualizar el gráfico en el canvas
    canvas.draw()
    
# Ejecutar la aplicación
app.mainloop()





