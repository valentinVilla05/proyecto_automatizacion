from tkinter import *
from tkinter import ttk
from main import main
import threading

# Flags para controlar la cancelación
cancelar = False
thread = None

def llamar_main():
    global thread, cancelar
    cancelar = False # Declaramos a False para que se ejecute el hilo
    threading.Thread(target=ejecutar_main).start()
    
def ejecutar_main():    
    main(lambda: cancelar) # Llamamos a la función main y le pasamos el flag de cancelación
    
    
def terminar_ejecucion():
    global cancelar
    cancelar = True # Cambioamos el estado de la flag a True para que el hilo se detenga
    print("Cancelando ejecución...") # Mensaje de cancelación
    root.destroy() # Cerramos la ventana de la GUI
    


# GUI    
root = Tk()
root.title("Automatización de entradas") # Titulo de la ventana
root.geometry("400x200") # Tamaño de la ventana

frm = ttk.Frame(root, padding=20)
frm.grid()

ttk.Label(frm, text="Automatización de entradas con IA").grid(column=0, row=0, columnspan=2, pady=10)

ttk.Button(frm, text="Iniciar", command=llamar_main).grid(column=0, row=1, padx=10)
ttk.Button(frm, text="Cerrar", command=terminar_ejecucion).grid(column=1, row=1, padx=10)

root.mainloop()