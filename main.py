from amazon.api import search_items
from promptAI.chatgpt import promptChatGPT
from promptAI.copilot import promptCopilot
from wordpress.post import newEntrada
import undetected_chromedriver as uc
from var_config import *
import requests
import re
import os

def main(comprobar_cancelacion=lambda: cancelar):
    lista_articulos = [
        "Modernos Ventilador de Techo con Luz, 48cm Ventilador de Techo sin Aspascon luz y Mando a Distancia, Ventiladores de Techo Silencioso con Luz LED Motor CC Reversible para Dormitorio, Salón ",
        "JARDIN202 - Ventilador de Techo LED con 4 Aspas 3500-4000-6500K Temporizador, 6 Velocidades, Aspas retráctiles | Tarifa (Blanco)"
    ]
    articulos_fallidos = []
    articulos_exitosos = []
    
    options = uc.ChromeOptions()
    options.headless = False  # Agregado manualmente para evitar el error interno
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options, use_subprocess=True)



    for articulo in lista_articulos:
        # Comprobamos que el usuario no haya cancelado la ejecución
        if comprobar_cancelacion():
            print("Ejecución cancelada por el usuario.")
            print("Terminando articulo en proceso...")
            driver.quit()
            break
        
        print(f"🔍 Buscando artículo: {articulo}")
        data = search_items(articulo)
        if data:
            title, reviews, image_url, description, enlace = data
            # Creamos el directorio de salida si no existe
            directorio = "imagenes"
            if not os.path.exists(directorio):
                os.makedirs(directorio)
            
            #Decargamos la imagen
            nombre_limpio = re.sub(r'[\\/*?:"<>|]', "", title) # Limpiar el título para que sea un nombre de archivo válido
            nombre_imagen = os.path.join(directorio, f"{nombre_limpio}.jpg")
            
            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    with open(nombre_imagen, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Imagen descargada: {nombre_imagen}")
                else: 
                    print(f"❌ Error HTTP {response.status_code} al descargar la imagen de: {title}")
            except Exception as e:
                print(f"❌ Excepción al descargar la imagen de {title}: {e}")
                
                
            exito = promptChatGPT(title, reviews, image_url, description, enlace, driver)

            if exito:
                articulos_exitosos.append(articulo)
                print(f"✅ Artículo procesado exitosamente: {articulo}")
            if not exito:
                print("❌ ChatGPT falló. Probando con Copilot...")
                exito_copilot = promptCopilot(title, reviews, image_url, description, enlace, driver)
                if exito_copilot:
                    articulos_exitosos.append(articulo)
                    print(f"✅ Artículo procesado exitosamente con Copilot: {articulo}")
                else: 
                    articulos_fallidos.append(articulo)
                    print(f"❌ Artículo fallido: {articulo}")
            
        else:
            print("⚠️ Artículo no encontrado.")
    
    print(f"Artículos exitosos: {articulos_exitosos}")
    print(f"Artículos fallidos: {articulos_fallidos}")
            

if __name__ == "__main__":
    main()