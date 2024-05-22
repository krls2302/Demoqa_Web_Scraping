from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException
import time
import os

def scroll_ven(element_locator):
    increment = 500  # Incremento en píxeles para desplazarse
    current_position = 0
    end_of_page = False
    
    while True:
        try:
            # Intentar encontrar y hacer clic en el elemento
            element = driver.find_element(*element_locator)
            driver.execute_script("arguments[0].scrollIntoView();", element)
            element.click()
            break
        except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException):
            # Si no encuentra el elemento o no se puede hacer clic, sigue desplazándose
            current_position += increment
            driver.execute_script("window.scrollBy(0, {});".format(increment))
            time.sleep(1)
            
            # Verificar si ha llegado al final de la página
            new_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
            if current_position >= new_position:
                if end_of_page:  # Si ya ha llegado al final de la página antes, salir del bucle
                    break
                end_of_page = True

def scroll_into_middle(locator):
    element = driver.find_element(*locator)
    driver.execute_script("arguments[0].scrollIntoView({ behavior: 'auto', block: 'center' });", element)

def safe_find_element(by, value):
    while True:
        try:
            if value =="state" or value == "City":
                element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, value)))
                return element
            element = driver.find_element(by, value)
            excepcion = ["dateOfBirthInput", "react-datepicker__month-select",
                            "react-datepicker__year-select", 
                            "//div[contains(@class, 'react-datepicker__day') and text()='26' and not(contains(@class, 'react-datepicker__day--outside-month'))]"]
            if value in excepcion:
                return element
            scroll_into_middle((by, value))
            return element
        except (ElementNotInteractableException, NoSuchElementException, ElementClickInterceptedException) as e:
            print(f"Error al encontrar el elemento {value}: {e}")
            scroll_ven((by, value))

# Ruta de la imagen a cargar
ruta_imagen = "/home/krls/Descargas/Python-logo.png"

driver = webdriver.Chrome()
driver.maximize_window()

driver.get("https://demoqa.com/automation-practice-form")

try:
    firstName = safe_find_element(By.ID, "firstName")
    firstName.send_keys("krls")

    lastName = safe_find_element(By.ID, "lastName")
    lastName.send_keys("chavita")

    userEmail = safe_find_element(By.ID, "userEmail")
    userEmail.send_keys("cchavita@gmail.com")

    male_radio = safe_find_element(By.CSS_SELECTOR, ".custom-control-label")
    male_radio.click()

    userNumber = safe_find_element(By.ID, "userNumber")
    userNumber.send_keys("3025839501")

    time.sleep(1)

    dateOfBirthInput = safe_find_element(By.ID, "dateOfBirthInput")
    dateOfBirthInput.click()

    time.sleep(1)

    month_dropdown = safe_find_element(By.CLASS_NAME, 'react-datepicker__month-select')
    select_month = Select(month_dropdown)
    select_month.select_by_value("0")

    time.sleep(1)

    year_dropdown = safe_find_element(By.CLASS_NAME, 'react-datepicker__year-select')
    select_year = Select(year_dropdown)
    select_year.select_by_value("1994")

    time.sleep(1)

    dia_select = safe_find_element(By.XPATH, "//div[contains(@class, 'react-datepicker__day') and text()='26' and not(contains(@class, 'react-datepicker__day--outside-month'))]")
    dia_select.click()

    time.sleep(1)

    select_subject = safe_find_element(By.ID, 'subjectsInput')
    select_subject.click()
    time.sleep(1)
    select_subject.send_keys("Computer Science")
    select_subject.send_keys(Keys.TAB)

    time.sleep(1)

    hobies = safe_find_element(By.CSS_SELECTOR, 'label[for="hobbies-checkbox-2"]')
    hobies.click()

    time.sleep(1)

    upload_element = safe_find_element(By.ID, "uploadPicture")
    upload_element.send_keys(os.path.abspath(ruta_imagen))

    time.sleep(1)

    currentAddress = safe_find_element(By.ID, "currentAddress")
    currentAddress.send_keys("Prueba de selenium en plataforma de demoqa")

    time.sleep(1)

    state = safe_find_element(By.ID, 'state')
    state.click()
    
    # Esperar a que las opciones se carguen y seleccionar la opción con el valor 'NFC'
    options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id^="react-select"]'))
    )

    for option in options:
        if 'NCR' in option.text:
            option.click()
            break

    time.sleep(1)

    city = safe_find_element(By.ID, 'city')
    city.click()
    # Esperar a que las opciones se carguen y seleccionar la opción con el valor 'NFC'
    options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[id^="react-select"]'))
    )

    for option in options:
        if 'Delhi' in option.text:
            option.click()
            break
    
    time.sleep(1)

    submit = safe_find_element(By.ID, 'submit')
    submit.click()

    time.sleep(2)

    modal = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@role="dialog"][@aria-modal="true"]'))
)

    # Desplazar el modal hacia arriba
    driver.execute_script("arguments[0].style.top = '-300px';", modal)
    time.sleep(1)

    close_button = safe_find_element(By.ID, 'closeLargeModal')
    close_button.click()


    time.sleep(3)

    driver.quit()

except Exception as e:
    print("Se produjo un error general:", e)
