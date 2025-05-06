import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


def cerrarVentanaEmergente(driver):
    # Manejar posible botón emergente de inicio de sesión
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="radix-«r1a»"]/div/div[1]/div/button'))).click()
        print("Cerrando ventana emergente...")
    except:
        print("No se encontró ventana emergente.")

def waitForResponseChatGPT(driver, timeout=100, interval=1):
    end_time = time.time() + timeout
    last_text = ""
    estable = 0
    
    while time.time() < end_time:
        try:
            input_prompt = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "prompt-textarea"))
            )
            responses = driver.find_elements(By.TAG_NAME, "code")
            text = responses[-1].text.strip() # Cogemos siempre el último bloque de codigo que nos haya dado
            
            if text == last_text:
                estable += 1
                if estable >= 3:
                    time.sleep(2)
                    if text.endswith("</html>"):
                        print("Esperando respuesta...")
                        print("La respuesta está completa") 
                        return text
                    else:
                        try:
                            # Buscar botón "Continue Generating"
                            continue_buttons = driver.find_elements(By.XPATH, "//*[contains(text(), 'Continue generating')]")
                            if continue_buttons:
                                print("Clickeando en 'Continue generating'...")
                                continue_buttons[0].click()
                            else:
                                print("No se encontró botón 'Continue generating', enviando prompt manual...")
                                cerrarVentanaEmergente(driver)
                                # Enviar prompt manualmente
                                input_prompt = driver.find_element(By.ID, "prompt-textarea")
                                prompt = "No dejes el código a medias, dámelo completo, por favor."
                                input_prompt.send_keys(prompt)
                                input_prompt.send_keys(Keys.ENTER)
                        except Exception as e:
                            print(f"Error al manejar continuación o envío: {e}")

            else:
                estable = 0
                last_text = text
                print("Esperando respuesta...")
                time.sleep(3)
            
        except Exception as e:
            print(f"Error al obtener la respuesta: {e}")
        
        time.sleep(interval)
    
    print("Esperando la respuesta completa.")
    return last_text


def waitForResponseCopilot(driver, timeout=100, interval=1):
    end_time = time.time() + timeout
    last_text = ""
    estable = 0
    
    while time.time() < end_time:
        try:
            input_prompt = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="userInput"]'))
            )
            responses = driver.find_elements(By.TAG_NAME, "code")
            text = responses[-1].text.strip() # Cogemos siempre el último bloque de codigo que nos haya dado
            
            if text == last_text:
                estable += 1
                if estable >= 3:
                    time.sleep(2)
                    if text.strip().lower().find("</html>") != -1:
                        print("Esperando respuesta...")
                        print("La respuesta está completa") 
                        return text
                    else:
                        input_prompt = driver.find_element(By.XPATH, "//*[@id=\"userInput\"]")
                        prompt = "No dejes el código a medias, dámelo completo, por favor."
                        input_prompt.send_keys(prompt)
                        time.sleep(1)
                        input_prompt.send_keys(Keys.ENTER)
 
            else:
                estable = 0
                last_text = text
                print("Esperando respuesta...")
                time.sleep(3)
            
        except Exception as e:
            print(f"Error al obtener la respuesta: {e}")
        
        time.sleep(interval)
    
    print("Esperando la respuesta completa.")
    return last_text

