from amazon.api import search_items
from promptAI.chatgpt import promptChatGPT
# from promptAI.copilot import promptCopilot
from wordpress.post import newEntrada
import undetected_chromedriver as uc

def main():
    lista_articulos = [
        "Cecotec Ventilador de Techo con Luz...",
        "ABRILA TODOLAMPARA Ventilador de techo..."
    ]
    
    options = uc.ChromeOptions()
    driver = uc.Chrome(headless=False, use_subprocess=False, options=options)

    for articulo in lista_articulos:
        print(f"🔍 Buscando artículo: {articulo}")
        data = search_items(articulo)
        if data:
            title, reviews, image_url, description, enlace = data
            promptChatGPT(title, reviews, image_url, description, enlace, driver)
        else:
            print("⚠️ Artículo no encontrado.")

if __name__ == "__main__":
    main()