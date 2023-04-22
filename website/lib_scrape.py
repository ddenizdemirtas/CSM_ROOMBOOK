from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup 

class LibraryScraper:
    
    
    
    available_slots = {}

        


    def check_availability(self, slot):

            splitted = slot.split()
            if splitted[-1] == 'Available':
                return True
            
            return False


    def format_data(self, data):


        data = " ".join(data)
        split_data = data.split(',')
        split_data.pop(1)
        clean_data = [s.replace(',', '') for s in split_data]
        final_data = ' '.join(clean_data)

        return final_data



    def scrape_availabilities(self):

        # driver setup 
        driver = uc.Chrome()
        driver.options.add_argument('--headless')
        library_url = 'https://berkeley.libcal.com/allspaces'
        driver.get(library_url)
        # wait setup
        div = "s-lc-8862"
        wait = WebDriverWait(driver=driver, timeout=30)
        get_url = driver.current_url
        wait.until(EC.url_to_be(library_url))
        
        if get_url == library_url:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, features="html.parser")
            wait.until(EC.presence_of_all_elements_located((By.ID, "time_grid_cont")))

            for i in range(7):
                table = soup.find("div", {"id" : div})
                contents = table.find("table").find_all('tr')
                self.available_slots[div] = []
                for content in contents:
                    availability_parent = content.find_all("div", {"class" : "fc-timeline-event-harness"})
                    
                    for a in availability_parent:
                        
                        availability = a.findChildren("a")
                        availability = availability[0]["aria-label"]

                        availability = availability.split()
                        availability.pop()
                        availability = self.format_data(availability)
                        self.available_slots[div].append(availability)


                        # Filter available
                        # if self.check_availability(availability):
                        #     availability = availability.split()
                        #     availability.pop()
                        #     availability = self.format_data(availability)
                        #     self.available_slots.append(availability)

                       

                        
                div= div[:-1] + str(int(div[-1]) + 1) if div[-1].isdigit() else div


       
        with open("/Users/denizdemirtas/Desktop/CSM_RoomBook/slots", "w") as f:
            
            for key, value in self.available_slots.items():
                f.write(f"{key}: {value}\n")

        exit()
        
        

    def make_reservation(self, reservation, library_ID, username, password):

        # driver setup 
        driver = uc.Chrome()
        driver.options.add_argument('--headless')
        library_url = 'https://berkeley.libcal.com/spaces?lid='
        div = library_ID[-4:]
        library_url += div
        driver.get(library_url)
        
        # wait setup
        wait = WebDriverWait(driver=driver, timeout=30)
        get_url = driver.current_url
        wait.until(EC.url_to_be(library_url))
        
        if get_url == library_url:
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, features="html.parser")

            # wait until page loads
            wait.until(EC.presence_of_all_elements_located((By.ID, "time_grid_cont")))
            
            #find the slot that the user wants to reserve and click on it (under work)
            #fix the reservation input, it needs to have the day and the time too. 
            driver.find_element(by=By.XPATH, value=f'//*[@aria-label={reservation}]').click()

            # wait until the submit button is clickable
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit_times"]')))

            
            
            # click the submit button 
            submit_time_button = driver.find_element(by=By.XPATH, value='//*[@id="submit_times"]')
            print("DEBUG: button = ", submit_time_button)
            submit_time_button.click()
           
           # wait until inpput fields are located
            while True:

                try: 

                    input_field = driver.find_element(By.ID, value='username')
                    break
                    
                except:

                    print("Element not found, retrying")

            input_field.send_keys(username)

            # find password field
            password_field = driver.find_element(By.ID, value='password')
            password_field.send_keys(password)

            # find submit button
            submit_cal_ID_button = driver.find_element(by=By.XPATH, value='//*[@id="submit"]')
            submit_cal_ID_button.click()

            while True:

                try: 

                    trust_browser_button = driver.find_element(By.ID, value='trust-browser-button')
                    break
                    
                except:

                    print("Element not found, retrying")
            
            trust_browser_button.click()

            while True:

                try: 
                    accept_policy_button = driver.find_element(By.CLASS_NAME, value='button--full')
                    break
                    
                except:

                    print("Element not found, retrying")

            accept_policy_button.click()


            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn btn-primary")))
            make_reservation_button = driver.find_element(by=By.CLASS_NAME, value="btn btn-primary")
            make_reservation_button.click()



        

# scraper = LibraryScraper()
# # scraper.make_reservation("5:00pm Sunday 2023 - 110MB - Available", "s-lc-8863", 'denizdemirtas', 'PradaBagCauseTheyPradaMe03_')
# scraper.scrape_availabilities()
