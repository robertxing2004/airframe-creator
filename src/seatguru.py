from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class ConfigurationFinder:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--no-sandbox")
        self.options.page_load_strategy = 'normal'

    def scrape(self, operator, aircraft):
        driver = webdriver.Chrome(options=self.options)
    
        try:
            driver.get("https://www.seatguru.com/browseairlines/browseairlines.php")
            link = driver.find_element( By.XPATH, f"//div[@class='browseAirlines']//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{operator.lower()}')]")
            driver.get(link.get_attribute('href'))

          
            wrapper = driver.find_element(By.ID, "wrapper")
            page = wrapper.find_element(By.ID, "page")
            home_center = page.find_element(By.CLASS_NAME, "home_center")
            content = home_center.find_element(By.ID, "content")
            container = content.find_element(By.CLASS_NAME, "container")
            content_narrow = container.find_element(By.CLASS_NAME, "content-narrow.overviewContainer.boxTop17")

            configs = content_narrow.find_elements(By.XPATH, f"//div[contains(@class, 'aircraft_seats')]/a[contains(text(), '{aircraft}') and contains(@href, '{aircraft}')]/..")
            if len(configs) > 1:
                print(f"Found multiple configurations for {operator} {aircraft}:")
                total_seats = []
                for config, seats in enumerate(configs):
                    first = 0
                    biz = 0
                    prem = 0
                    eco = 0
                    seat_classes = seats.find_elements(By.CLASS_NAME, "seat_class")
                    for seat_class in seat_classes:
                        count = seat_class.find_element(By.CLASS_NAME, "seat_count").text
                        class_type = seat_class.text.replace(count, '').strip()
                        if "First" in class_type:
                            first = int(count)
                        elif "Business" in class_type:
                            biz = int(count)
                        elif "Premium" in class_type:
                            prem = int(count)
                        elif "Economy" in class_type:
                            eco = int(count)
                    total_seats.append(first + biz + prem + eco)
                    print(f"{config + 1}. {(str(first) + " First | ") if first > 0 else ""}{(str(biz) + " Business | ") if biz > 0 else ""}{(str(prem) + " Premium | ") if prem > 0 else ""}{(str(eco) + " Economy") if eco > 0 else ""}")
                choice = int(input(f"Select desired configuration: "))
                seats = total_seats[choice]
            else:
                first = 0
                biz = 0
                prem = 0
                eco = 0
                seat_classes = configs[0].find_elements(By.CLASS_NAME, "seat_class")
                for seat_class in seat_classes:
                    count = seat_class.find_element(By.CLASS_NAME, "seat_count").text
                    class_type = seat_class.text.replace(count, '').strip()
                    if "First" in class_type:
                        first = int(count)
                    elif "Business" in class_type:
                        biz = int(count)
                    elif "Premium" in class_type:
                        prem = int(count)
                    elif "Economy" in class_type:
                        eco = int(count)
                seats = first + biz + prem + eco

            return seats
        
        except Exception as e:
          print(f"Configuration {operator} {aircraft} not found: {str(e)}")
          return 0
            
        finally:
            driver.quit()