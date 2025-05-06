import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from var_config import *
import time


def subirImagen():
    options = uc.ChromeOptions()
    options.headless = False  # Agregado manualmente para evitar el error interno
    options.add_argument("--disable-gpu") # Para compatibilidad
    driver = uc.Chrome(options=options, use_subprocess=True)
    
    driver.get("https://ventiladoresdetechos.es/wp-admin/upload.php")
    
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
            
        # Click en añadir archivo
        boton_anadir = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="wp-media-grid"]/a')))
        boton_anadir.click()
        boton_archivo = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__wp-uploader-id-1"]')))
        boton_archivo.click()
        input_file = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
        input_file.send_keys("/home/valentin05/Documents/python_pruebas/proyecto_automatizacion/imagenes/imagen_prueba.jpg")
        time.sleep(2)
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        return False
    
    
    
subirImagen()