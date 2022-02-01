from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from .source import Adv_source


class Workday(Adv_source):

    def get_results(self):
        """Checks for new advertisements, returns dictionary with results"""
        self.last_checked_date=datetime.date.today().isoformat()

        # Open new session, after page loads wait until the initial HTML document is completely loaded and parsed, and discard loading of stylesheets, images and subframes.
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"

        with Firefox() as driver:
            adverts={}
            
            for position in self.positions:
                driver.get(self.source_website)

                # Find search field, clear and input query
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[data-automation-id='keywordSearchInput']"))).clear()
                driver.find_element(By.CSS_SELECTOR,"input[data-automation-id='keywordSearchInput']").send_keys(position)
                
                # Find localisation button, input city, and choose it from drop-down menu
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-automation-id='distanceLocation']"))).click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"input[data-automation-id='searchInput']"))).send_keys("London")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"li[data-automation-id='menuItem-London']"))).click()

                # Confirm search
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"button[data-automation-id='keywordSearchButton']"))).click()
                WebDriverWait(driver,1000)
                # Find search results on every possible page
                try:
                    while WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"a[data-automation-id='jobTitle']"))):
                        results=driver.find_elements(By.CSS_SELECTOR,"a[data-automation-id='jobTitle']")

                        # Grab hrefs and extract job numbers, create dictionary with titles
                        for result in results:
                            href=result.get_attribute("href")
                            adverts[f'{href.rsplit("_",1)[1]}']={'title':result.text,'href': href}

                        # Go to next page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.find_element(By.CLASS_NAME, "wd-icon-chevron-right-small").click()
                   
                except: pass
            return adverts




