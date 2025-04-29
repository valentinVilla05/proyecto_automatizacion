from tkinter import *
from tkinter import ttk
from main import main
import threading

def lanzar_main():
    threading.Thread(target=main).start()
    
root = Tk()
root.title("Automatización de entradas") # Titulo de la ventana
root.geometry("400x200") # Tamaño de la ventana

frm = ttk.Frame(root, padding=20)
frm.grid()

ttk.Label(frm, text="Automatización de entradas con IA").grid(column=0, row=0, columnspan=2, pady=10)

ttk.Button(frm, text="Iniciar", command=lanzar_main).grid(column=0, row=1, padx=10)
ttk.Button(frm, text="Cerrar", command=root.destroy).grid(column=1, row=1, padx=10)

root.mainloop()