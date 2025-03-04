from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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

    def scrape(self, operator, registration):
        driver = webdriver.Chrome(options=self.options)
        wait = WebDriverWait(driver, 5)
    
        try:
            driver.get('https://rzjets.net/aircraft/')  
                
            content = wait.until(EC.presence_of_element_located((By.ID, "container")))
            registration_field = content.find_element(By.NAME, "registry")
            registration_field.send_keys(registration)
            submit_button = content.find_element(By.NAME, "submitB")
            submit_button.click()

            table = wait.until(EC.visibility_of_element_located((By.ID, "tableList")))
            tbody = table.find_element(By.TAG_NAME, "tbody")
            row = tbody.find_element(By.XPATH, f"//tr[count(td) = 9]")

            headers = ["Registration", "Aircraft", "MSN", "Tail", "Engine", "Name", "Operator", "Built", "SELCAL", "ICAO24"]
            value_cells = row.find_elements(By.TAG_NAME, "td")
            values = [value.text.strip() for value in value_cells]
            icao_row = row.find_element(By.XPATH, "./following-sibling::tr[1]")
            values.append(icao_row.find_element(By.XPATH, "./td[last()]").text)
            
            data = dict(zip(headers, values))

            return data
        
        except Exception as e:
          print(f"Airframe {registration} not found: {str(e)}")
          return 0
            
        finally:
            driver.quit()