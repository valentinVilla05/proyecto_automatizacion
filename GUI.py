from tkinter import *
from tkinter import ttk
from main import main
import threading
import var_config

# Flags para controlar la cancelación
cancelar = False

def llamar_main():
    global cancelar
    cancelar = False

    # Construir el diccionario de configuración
    config = {
        "nombre_articulo": entry_articulo.get(),
        "partner_tag": entry_tag.get(),
        "wordpress_url": entry_url.get().strip(),
        "wordpress_email": entry_username.get(),
        "wordpress_password": entry_password.get(),
    }

    print(f"🧪 Config pasada a main: {config}")

    # Iniciar el hilo para ejecutar la función main
    threading.Thread(target=ejecutar_main, args=(config,)).start()

def ejecutar_main(config):
    main(lambda: cancelar, config)

def terminar_ejecucion():
    global cancelar
    cancelar = True
    print("Cancelando ejecución...")

def actualizar_variables():
    # Actualizamos las variables de configuración
    var_config.NOMBRE_ARTICULO = entry_articulo.get()
    var_config.PARTNER_TAG = entry_tag.get()
    var_config.WORDPRESS_URL = entry_url.get().strip()
    var_config.WORDPRESS_EMAIL = entry_username.get()
    var_config.WORDPRESS_PASSWORD = entry_password.get()

    # Llamar a la función para pasar la configuración a la ejecución de main
    llamar_main()

def cerrar_ventana():
    global cancelar
    cancelar = True
    print("Cancelando ejecución...")
    ventana.destroy()

# GUI
ventana = Tk()
ventana.title("Automatización de Productos Amazon")

# ----------- FRAME CONTENEDOR -------------
frame_formulario = ttk.Frame(ventana, padding=20)
frame_formulario.pack(padx=10, pady=10)

# Nombre del artículo
ttk.Label(frame_formulario, text="Nombre de artículo:").pack(pady=5)
entry_articulo = ttk.Entry(frame_formulario)
entry_articulo.insert(0, var_config.NOMBRE_ARTICULO)
entry_articulo.pack()

# Tag de afiliados
ttk.Label(frame_formulario, text="Tag de afiliados:").pack(pady=5)
entry_tag = ttk.Entry(frame_formulario)
entry_tag.insert(0, var_config.PARTNER_TAG)
entry_tag.pack()

# URL de la página de WordPress
ttk.Label(frame_formulario, text="URL de la página de WordPress:").pack(pady=5)
entry_url = ttk.Entry(frame_formulario)
entry_url.insert(0, var_config.WORDPRESS_URL)
entry_url.pack()

# Email de WordPress
ttk.Label(frame_formulario, text="Email de WordPress:").pack(pady=5)
entry_username = ttk.Entry(frame_formulario)
entry_username.insert(0, var_config.WORDPRESS_EMAIL)
entry_username.pack()

# Contraseña de WordPress
ttk.Label(frame_formulario, text="Contraseña de WordPress:").pack(pady=5)
entry_password = ttk.Entry(frame_formulario, show="*")
entry_password.insert(0, var_config.WORDPRESS_PASSWORD)
entry_password.pack()

# Botón para iniciar la automatización
ttk.Button(frame_formulario, text="Iniciar Automatización", command=actualizar_variables).pack(pady=20)
ttk.Button(frame_formulario, text="Cancelar ejecucion", command=terminar_ejecucion).pack(pady=20)   
ttk.Button(frame_formulario, text="Cancelar ejecucion y cerrar ventana", command=cerrar_ventana).pack(pady=20)   

# Ejecutar ventana
ventana.mainloop()
