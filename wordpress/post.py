from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import html
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
        
def esperar_url_imagen(driver):
    """Espera hasta que el campo de URL tenga contenido."""
    for _ in range(20):  # Hasta 10 segundos (20 * 0.5s)
        try:
            input_url = driver.find_element(By.ID, 'attachment-details-two-column-copy-link')
            url = input_url.get_attribute("value")
            if url:
                return url
        except:
            pass
        time.sleep(0.5)
    return None

def subirImagen(driver, directorio, nombre_imagen, WORDPRESS_URL):
    print(f"📁 Directorio recibido: {directorio}")
    print(f"🖼️ Nombre de imagen recibido: {nombre_imagen}")
    print(f"🌐 WORDPRESS URL: {WORDPRESS_URL}")

    url_parseada = WORDPRESS_URL.rstrip("/")
    final_url = url_parseada + "/wp-admin/upload.php" if not url_parseada.endswith("wp-admin/upload.php") else url_parseada
    print(f"📦 URL final para subir imágenes: '{final_url}'")
    driver.get(final_url)

    try:
        # 1. Hacer clic en "Añadir nuevo"
        boton_anadir = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="wp-media-grid"]/a'))
        )
        boton_anadir.click()

        # 2. Seleccionar archivo
        input_file = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]'))
        )
        ruta_completa = os.path.abspath(nombre_imagen)
        print(f"📁 Ruta completa del archivo: {ruta_completa}")
        if not os.path.isfile(ruta_completa):
            print(f"❌ El archivo no existe en la ruta especificada: {ruta_completa}")
            return False

        input_file.send_keys(ruta_completa)

        # 3. Esperar que aparezca la lista de archivos
        contenedor = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.attachments"))
        )

        # 4. Hacer clic en la imagen subida (la más reciente)
        primer_li = WebDriverWait(contenedor, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.attachment:first-child"))
        )
        primer_li.click()

        # 5. Esperar que el panel lateral se cargue
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "attachment-details"))
        )

        # 6. Esperar que el campo tenga la URL
        url_imagen = esperar_url_imagen(driver)
        if not url_imagen:
            print("❌ No se pudo obtener la URL de la imagen.")
            return False

        print(f"✅ URL de la imagen: {url_imagen}")
        return url_imagen

    except Exception as e:
        print(f"❌ Error al subir la imagen: {e}")
        return False


def insertar_imagen_en_prompt(prompt, url_imagen):
    # Crear el HTML de la imagen
    imagen_html = f'<img src="{url_imagen}" alt="Imagen de producto" style="max-width:100%; height:auto; margin-bottom:20px;">'
    
    lineas = prompt.splitlines()
    nuevo_prompt = []

    imagen_insertada = False
    for linea in lineas:
        if not imagen_insertada and ("amazon.es" in linea or "amazon.com" in linea):
            nuevo_prompt.append(imagen_html)  # Insertar imagen antes del primer enlace a Amazon
            imagen_insertada = True
        nuevo_prompt.append(linea)

    # Si no hay enlace a Amazon, lo dejamos al final
    if not imagen_insertada:
        nuevo_prompt.insert(0, imagen_html)

    return "\n".join(nuevo_prompt)        
        
    
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
    if not imagen_url:
        print("❌ No se pudo subir la imagen. Se aborta la publicación.")
        return 
        
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
    prompt_modificado = insertar_imagen_en_prompt(prompt, imagen_url)
    enviar_prompt(input_code, prompt_modificado)
    
    
    
    time.sleep(10)  # Espera para ver el resultado antes de cerrar el navegador

    # Publicar entrada (descomenta cuando estés listo para publicar)
    # boton_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[1]/div/div[4]/button[2]")))
    # boton_publicar.click()
    # 
    # confirmar_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[2]/button")))
    # confirmar_publicar.click()
