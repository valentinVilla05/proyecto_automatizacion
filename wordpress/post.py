from datetime import datetime
from var_config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.parse

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

def newEntrada(title, prompt, driver, WORDPRESS_URL, WORDPRESS_EMAIL, WORDPRESS_PASSWORD):
        
    print("Ha entrado en la función newEntrada")
    print(f"🧪 URL que se usará: '{WORDPRESS_URL}'")
    
    url_parseada = WORDPRESS_URL.rstrip("/")
    if url_parseada.endswith("wp-admin/post-new.php"):
        final_url = url_parseada
    else:
        final_url = url_parseada + "/wp-admin/post-new.php"

    print(f"📦 URL final para abrir: '{final_url}'")
    driver.get(final_url)
    
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
    
    input_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inspector-textarea-control-0")))
    input_title.send_keys(title)
    
    input_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-content-0")))
    enviar_prompt(input_code, prompt)


    # Publicar entrada
    # boton_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[1]/div/div[4]/button[2]")))
    # boton_publicar.click()
    # 
    # confirmar_publicar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id=\"editor\"]/div/div[1]/div/div[2]/div[3]/div[2]/div/div/div[1]/div[2]/button")))
    # confirmar_publicar.click()
    
    
    

