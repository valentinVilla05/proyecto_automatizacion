import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def waitForResponseChatGPT(driver, timeout=60, interval=1):
    end_time = time.time() + timeout
    last_text = ""
    estable = 0
    
    while time.time() < end_time:
        try:
            response = driver.find_element(By.TAG_NAME, "code")
            text = response.text.strip()
            
            if text == last_text:
                estable += 1
                if estable >= 3:
                    print("La respuesta está completa")
                    return text
            else:
                estable = 0
                last_text = text
                print("Esperando respuesta...")
            
        except Exception as e:
            print(f"Error al obtener la respuesta: {e}")
        
        time.sleep(interval)
    
    print("Esperando la respuesta completa.")
    return last_text