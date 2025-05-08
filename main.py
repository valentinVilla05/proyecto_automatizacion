from amazon.api import search_items
from promptAI.chatgpt import promptChatGPT
from promptAI.copilot import promptCopilot
from wordpress.post import newEntrada
import undetected_chromedriver as uc
import requests
import re
import unicodedata
import os

def limpiar_nombre_archivo(nombre):
    nombre = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode('utf-8')
    nombre = re.sub(r'[^\w\s-]', '', nombre).strip().lower()
    nombre = re.sub(r'[\s]+', '_', nombre)
    return nombre

def main(comprobar_cancelacion=lambda: False, config=None):
    if config is None:
        print("❌ No se proporcionó configuración.")
        return
    
    NOMBRE_ARTICULO = config.get("nombre_articulo", "").strip()
    PARTNER_TAG = config.get("partner_tag", "").strip()
    WORDPRESS_URL = config.get("wordpress_url", "").strip()
    WORDPRESS_EMAIL = config.get("wordpress_email", "").strip()
    WORDPRESS_PASSWORD = config.get("wordpress_password", "").strip()
    
    print(f"🔗 URL recibida en main: '{WORDPRESS_URL}'")

    if not WORDPRESS_URL:
        print("❌ WORDPRESS_URL no es válida.")
        return
    
    lista_articulos = [
        "Modernos Ventilador de Techo con Luz, 48cm Ventilador de Techo sin Aspascon luz y Mando a Distancia, Ventiladores de Techo Silencioso con Luz LED Motor CC Reversible para Dormitorio, Salón ",
        "JARDIN202 - Ventilador de Techo LED con 4 Aspas 3500-4000-6500K Temporizador, 6 Velocidades, Aspas retráctiles | Tarifa (Blanco)"
    ]
    articulos_fallidos = []
    articulos_exitosos = []
    
    options = uc.ChromeOptions()
    options.headless = False
    options.add_argument("--disable-gpu")
    driver = uc.Chrome(options=options, use_subprocess=True)

    for articulo in lista_articulos:
        if comprobar_cancelacion():
            print("⛔ Ejecución cancelada por el usuario.")
            driver.quit()
            break

        print(f"🔍 Buscando artículo: {articulo}")
        data = search_items(articulo)
        if not data:
            print("⚠️ Artículo no encontrado.")
            articulos_fallidos.append(articulo)
            continue

        title, reviews, image_url, description, enlace = data
        directorio = f"imagenes_" + NOMBRE_ARTICULO
        if not os.path.exists(directorio):
            os.makedirs(directorio)

        nombre_limpio = limpiar_nombre_archivo(title)
        nombre_imagen = os.path.join(directorio, f"{nombre_limpio}.jpg")

        try:
            response = requests.get(image_url, timeout=10)
            if response.status_code == 200:
                with open(nombre_imagen, 'wb') as f:
                    f.write(response.content)
                print(f"✅ Imagen descargada: {nombre_imagen}")
            else:
                print(f"❌ Error HTTP {response.status_code} al descargar imagen.")
        except Exception as e:
            print(f"❌ Excepción al descargar la imagen: {e}")

        # Intentamos generar contenido con ChatGPT
        try:
            exito = promptChatGPT(
                title, reviews, image_url, description, enlace,
                driver, PARTNER_TAG, WORDPRESS_URL, WORDPRESS_EMAIL,
                WORDPRESS_PASSWORD, directorio, nombre_imagen)

            if not exito:
                raise Exception("ChatGPT no generó contenido.")
        
        except Exception as e:
            print(f"❌ ChatGPT falló: {e}")
            # Fallback a Copilot
            try:
                exito = promptCopilot(
                    title, reviews, image_url, description, enlace,
                    driver, PARTNER_TAG, WORDPRESS_URL,
                    WORDPRESS_EMAIL, WORDPRESS_PASSWORD
                )
                if not exito:
                    raise Exception("Copilot también falló.")
            except Exception as e:
                print(f"❌ Copilot falló: {e}")
                articulos_fallidos.append(articulo)
                continue  # No pasamos a la publicación

        # Si el contenido fue generado por ChatGPT o Copilot, intentamos publicarlo
        try:
            resultado = newEntrada(
                title, None, driver,
                WORDPRESS_URL, WORDPRESS_EMAIL, WORDPRESS_PASSWORD,
                directorio, nombre_imagen
            )
            if not resultado:
                raise Exception("Error al publicar el contenido.")
            articulos_exitosos.append(articulo)
            print(f"✅ Artículo publicado: {articulo}")

        except Exception as e:
            print(f"❌ Error al publicar: {e}")
            articulos_fallidos.append(articulo)

    print(f"📦 Artículos exitosos: {articulos_exitosos}")
    print(f"🗃️ Artículos fallidos: {articulos_fallidos}")
    driver.quit()

if __name__ == "__main__":
    main()
