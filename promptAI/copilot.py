from promptAI.helper import waitForResponseCopilot
from wordpress.post import newEntrada
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyperclip

def promptCopilot(title, reviews, image_url, description, enlace, driver, PARTNER_TAG, WORDPRESS_URL, WORDPRESS_EMAIL, WORDPRESS_PASSWORD):
    # Navegar a Copilot
    driver.get("https://copilot.microsoft.com/")

    try:

        # Intentar hacer clic en el campo de entrada si está oculto
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="userInput"]'))).click()
            print("Activando campo de texto...")
        except:
            print("Campo de texto ya estaba activo.")

        # Esperar a que el campo de entrada de Copilot esté disponible
        input_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "userInput"))
        )
        print("Campo de entrada encontrado.")

        # Esperar a que se cargue la búsqueda de productos
        espera_maxima = 30
        tiempo_esperado = 0
        while (title == "" or reviews == "" or image_url == "" or description == "") and tiempo_esperado < espera_maxima:
            print("Esperando a que se complete la búsqueda de productos...")
            print(f"DEBUG: Título: {title}, Reseñas: {reviews}, Imagen: {image_url}, Descripción: {description}")
            time.sleep(1)
            tiempo_esperado += 1

        if title == "" or reviews == "" or image_url == "" or description == "":
            print("❌ No se encontraron datos del producto. Saliendo...")
            return

        # Modificar reviews si es necesario
        if reviews in ["No Reviews", "none"]:
            reviews = "Sin reseñas"

        # Mensaje para ChatGPT
        mensaje = (
        f"De este producto, a continuación necesito que me hagas un artículo con al menos 1000 palabras. "
        f"Incluye también un boton con este enlace {enlace}, incluye tambien opiniones de usuarios, pero sin mencionar nombres ni apellidos; habla de usuarios en general. "
        f"Es importante que el artículo tenga un mínimo de 1000 palabras. "
        f"El título debe ser: {title}: ofertas y opiniones de usuarios. "
        f"Habla en tercera persona. No vendo el producto directamente. "
        f"Cada H2, H3 y H4 debe incluir el nombre del producto. "
        f"El artículo debe estar en HTML optimizado para SEO. No pongas ninguna fecha ni año. "
        f"Presta atención al uso adecuado de las mayúsculas. "
        f"Incorpora las siguientes palabras clave: Comprar, Vender, Precio, Oferta, Descuento, Barato, Mejor precio, "
        f"Cupones, Código de descuento, Envío gratuito, Liquidación, Promoción, Adquirir, Reservar, En stock, "
        f"Carrito de compra, Compra en línea, Ordenar ahora, Pagos, Factura, Comparar precios, Accesorios, "
        f"Tienda oficial, Garantía, Crédito, Financiación, Disponible ahora, Suscribirse, Catálogo, Inventario. "
        f"El contenido debe estar en HTML y optimizado para SEO. "
        f"Estructura semántica requerida: Schema.org TechArticle, Schema.org Product, HTML5 semántico optimizado, "
        f"Jerarquía clara de contenidos. "
        f"Elementos técnicos: Meta tags optimizados, Datos estructurados completos, URLs semánticas, "
        f"Estructura de navegación mejorada. "
        f"Experiencia de usuario optimizada: Navegación intuitiva, Contenido segmentado, FAQ expandible, Tablas informativas. "
        f"No agregues CSS ni imágenes. No añadas un apartado de 'contenido'."
        f"No añadas ninguna marca que indique que está hecho con IA. "
        )
        input_box.send_keys(mensaje)
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)
        
        time.sleep(4)

        # Esperar respuesta
        print("Esperando respuesta de Copilot...")
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[2]/div[2]/main/div[3]/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div[2]/button'))
            )
                        
            try:
                WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.TAG_NAME, "code"))
                )
                respuesta = waitForResponseCopilot(driver)
                
                if respuesta.strip() and respuesta.strip().find("</html>") != -1:
                    pyperclip.copy(respuesta)
                    newEntrada(title, respuesta, driver)
                    return True
                else:
                    print("❌ La respuesta estaba vacía, no se copió al portapapeles.")
                
            except Exception as e:
                print(f"❌ No se pudo obtener la respuesta de Copilot: {e}")
                return False
    
        except Exception as e:
            print(f"Ha habido un error generando la respuestas: {e}")
            return False

    except Exception as e:
        print(f"❌ Error durante la interacción con Copilot: {e}")
        return False

    finally:
        print("Proceso finalizado.")