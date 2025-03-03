from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from time import sleep
from dotenv import load_dotenv
import os

class AirframeFinder:
    def __init__(self):
        load_dotenv()
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.page_load_strategy = 'normal'
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')

    def login(self, username, password):
        driver = webdriver.Chrome(options=self.options)
        wait = WebDriverWait(driver, 5)

        if driver.find_elements(
            By.XPATH, "//small[contains(text(), 'Logged in as')]"
        ):
            return True
    
        try:
            driver.get('https://www.airframes.org/login')
            content = driver.find_element(By.ID, "content")
            username_field = wait.until(EC.presence_of_element_located((By.NAME, "user1")))
            password_field = content.find_element(By.NAME, "passwd1")
            
            username_field.send_keys(username)
            password_field.send_keys(password)
            
            login_button = content.find_element(By.NAME, "submit")
            login_button.click()
            
            wait.until(
                EC.presence_of_element_located((
                    By.XPATH, "//small[contains(text(), 'Logged in as')]"
                ))
            )
            return True
            
        except Exception as e:
          print(f"Login failed: {str(e)}")
          return False

    def scrape(self, registration):
        driver = webdriver.Chrome(options=self.options)
        wait = WebDriverWait(driver, 5)
    
        try:
            driver.get('https://www.airframes.org/')
            
            if self.username and self.password:
                if not self.login(self.username, self.password):
                    raise Exception("Login failed")
            
            sleep(2)
            content = wait.until(EC.presence_of_element_located((By.ID, "content")))
            registration_field = content.find_element(By.NAME, "reg1")
            registration_field.send_keys(registration)
            submit_button = content.find_element(By.NAME, "submit")
            submit_button.click()

            table = wait.until(EC.presence_of_element_located((
                By.XPATH, 
                "//p[contains(text(), 'Your query for aircraft registration')]/following::table[1]"
            )))
            tbody = table.find_element(By.TAG_NAME, "tbody")
            rows = tbody.find_elements(By.TAG_NAME, "tr")

            headers = rows[0].find_elements(By.TAG_NAME, "th")
            header_texts = [header.text.strip() for header in headers]
            
            values = rows[1].find_elements(By.TAG_NAME, "td")
            value_texts = [value.text.strip() for value in values]
            
            data = dict(zip(header_texts, value_texts))

            sleep(2)

            return data
        
        except Exception as e:
          print(f"Airframe {registration} not found: {str(e)}")
          return 0
            
        finally:
            driver.quit()