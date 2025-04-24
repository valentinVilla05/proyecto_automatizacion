from amazon.api import search_items
from promptAI.chatgpt import promptChatGPT
from promptAI.copilot import promptCopilot
from wordpress.post import newEntrada
import undetected_chromedriver as uc

def main():
    lista_articulos = [
        "Modernos Ventilador de Techo con Luz, 48cm Ventilador de Techo sin Aspascon luz y Mando a Distancia, Ventiladores de Techo Silencioso con Luz LED Motor CC Reversible para Dormitorio, Salón ",
        "JARDIN202 - Ventilador de Techo LED con 4 Aspas 3500-4000-6500K Temporizador, 6 Velocidades, Aspas retráctiles | Tarifa (Blanco)"
    ]
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(headless=False, use_subprocess=False, options=options)

    for articulo in lista_articulos:
        print(f"🔍 Buscando artículo: {articulo}")
        data = search_items(articulo)
        if data:
            title, reviews, image_url, description, enlace = data
            try:
                promptChatGPT(title, reviews, image_url, description, enlace, driver)
            except: 
                print("Ha habido un error con ChatGPT. Probando con Copilot...")
                promptCopilot(title, reviews, image_url, description, enlace, driver)
        else:
            print("⚠️ Artículo no encontrado.")

if __name__ == "__main__":
    main()