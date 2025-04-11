from datetime import datetime
from var_config import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def newEntrada(title, prompt, driver):
        
    print("Ha entrado en la función newEntrada")
    driver.get("https://ventiladoresdetechos.es/wp-admin/post-new.php")
    
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
    
    input_title = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inspector-textarea-control-0")))
    input_title.send_keys(title)
    
    input_code = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "post-content-0")))
    input_code.send_keys(prompt)

    #entradaAnadida = True
    #with open("log.txt", "a") as f:
    #    f.write(f"[{datetime.now()}] Procesando: {title}\n")
    #    if entradaAnadida:
    #        f.write(f"✅ Entrada añadida correctamente\n\n")
    #    else:
    #        f.write(f"❌ Error al añadir entrada o no se completó: {title}\n\n")
