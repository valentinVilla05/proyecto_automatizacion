from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse
import os

def enviar_prompt(input_element, prompt, espera=1):
    lineas = prompt.splitlines()
    buffer = ""
    max_caracteres = 300  

    for linea in lineas:
        if len(buffer + linea) > max_caracteres:
            input_element.send_keys(buffer)
            time.sleep(espera)
            buffer = ""
        buffer += linea + "\n"

    if buffer.strip():
        input_element.send_keys(buffer)
        
def subirImagen(driver, directorio, nombre_imagen, WORDPRESS_URL):
    print(f"📁 Directorio recibido: {directorio}")
    print(f"🖼️ Nombre de imagen recibido: {nombre_imagen}")

    print(f"WORDPRESS URL: {WORDPRESS_URL}")
    url_parseada = WORDPRESS_URL.rstrip("/")
    if url_parseada.endswith("wp-admin/upload.php"):
        final_url = url_parseada
    else:
        final_url = url_parseada + "/wp-admin/upload.php"

    print(f"📦 URL final para subir imagenes: '{final_url}'")
    driver.get(final_url)
        
    try:
        # Click en añadir archivo
        boton_anadir = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wp-media-grid"]/a')))
        boton_anadir.click()
        
        input_file = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        ruta_completa = os.path.join(directorio, nombre_imagen)
        print(f"📁 Ruta completa del archivo: {ruta_completa}")
        if not os.path.isfile(ruta_completa):
            print(f"❌ El archivo no existe en la ruta especificada: {ruta_completa}")
            return False

        input_file.send_keys(ruta_completa)
        
        # Esperamos hasta que se carguen las imágenes
        contenedor = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.attachments")))

        # Encuentra el primer <li class="attachment ...">
        primer_li = contenedor.find_element(By.CSS_SELECTOR, "li.attachment")

        # Haz clic directamente en el <li>, que selecciona la imagen
        primer_li.click()
        
        # Esperamos que la URL de la imagen esté disponible
        url_imagen = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'attachment-details-two-column-copy-link')))
        url_imagen = url_imagen.get_attribute("value") # Esto devuelve la URL de la imagen

        print(f"URL de la imagen: {url_imagen}")

        return url_imagen
    except Exception as e:
        print(f"❌ Error al subir la imagen: {e}")
        return False

def insertar_imagen(driver, url_imagen):
    #elemento_imagen = "<img src='" + url_imagen + "' alt='Im    agen' />"
    
    bloque_codigo = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.ID, "post-content-0")))
    
    contenido_codificado = bloque_codigo.get_attribute("value") # Esto devuelve el contenido HTML del textarea
    contenido_decodificado = html.unescape(contenido_codificado) # Decodificamos el contenido HTML (&gt; se convierte en >, etc.)

    # Buscamos el boton con la redireccoin a amazon para añadir la imagen antes
    elementos_amazon = driver.find_elements(By.XPATH, '//*[contains(@href, "amazon.es") or (self::button and .//a[contains(@href, "amazon.es")])]')
    
    # Si encontramos el enlace
    if elemento_enlace_amazon:
        elemento_amazon = elementos_amazon[0]
        
        # Creamos el elemento de la imagen
        imagen_html = f'<img src="{url_imagen}" alt="Imagen de producto" style="max-width:100%; height:auto; margin-bottom:20px;">'
        
        # Insertamos la imagen justo antes del elemento de Amazon       
        contenido_modificado = contenido_decodificado.replace(elemento_amazon.get_attribute("outerHTML"), imagen_html + "\n" + elemento_amazon.get_attribute("outerHTML"))

        # Actualizar el contenido en el <textarea>
        bloque_codigo.clear()  # Limpiar el <textarea>
        bloque_codigo.send_keys(contenido_modificado)
        
        print("Imagen insertada antes del primer enlace o botón de Amazon con éxito.")
    else:
        print("No se encontró un enlace o botón que contenga un enlace de Amazon.")
        
        
    
def login(driver, WORDPRESS_EMAIL, WORDPRESS_PASSWORD):
    email = WORDPRESS_EMAIL
    password = WORDPRESS_PASSWORD
    
    try: 
        if "wp-login.php" in driver.current_url:
            input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_login")))
            input_pass = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "user_pass")))
            input_submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wp-submit")))

            input_email.send_keys(email)
            input_pass.send_keys(password)
            input_submit.click()
        else:
            print("Sesión ya iniciada")
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        return False


def newEntrada(title, prompt, driver, WORDPRESS_URL, WORDPRESS_EMAIL, WORDPRESS_PASSWORD, directorio ,nombre_imagen):
        
    print("Ha entrado en la función newEntrada")
    print(f"🧪 URL que se usará: '{WORDPRESS_URL}'")
    
    url_parseada = WORDPRESS_URL.rstrip("/")
    if url_parseada.endswith("wp-login.php"):
        final_url = url_parseada
    else:
        final_url = url_parseada + "/wp-login.php"
    
    driver.get(final_url)
    
    login(driver, WORDPRESS_EMAIL, WORDPRESS_PASSWORD)
        
    imagen_url = subirImagen(driver, directorio, nombre_imagen, WORDPRESS_URL)    
        
    url_parseada = WORDPRESS_URL.rstrip("/")
    if url_parseada.endswith("wp-admin/post-new.php"):
        final_url = url_parseada
    else:
        final_url = url_parseada + "/wp-admin/post-new.php"
        
    print(f"📦 URL final para abrir: '{final_url}'")
    
    driver.get(final_url)
    
    input_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inspector-textarea-control-0")))
    input_title.send_keys(title)
    
    input_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-content-0")))
    enviar_prompt(input_code, prompt)
    
    insertar_imagen(driver, imagen_url)

    # Publicar entrada (descomenta cuando estés listo para publicar)
    # boton_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[1]/div/div[4]/button[2]")))
    # boton_publicar.click()
    # 
    # confirmar_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[2]/button")))
    # confirmar_publicar.click()
