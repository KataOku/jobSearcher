from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from .source import Adv_source


class Google(Adv_source):

    def get_results(self):
        """Checks for new advertisements, returns dictionary with results"""
        self.last_checked_date=datetime.date.today().isoformat()

        # Open new session, after page loads wait until the initial HTML document is completely loaded and parsed, and discard loading of stylesheets, images and subframes.
        caps = DesiredCapabilities().FIREFOX
        caps["pageLoadStrategy"] = "eager"
    
        with Firefox(capabilities=caps) as driver:
            adverts={}

            for position in self.positions:
                driver.get(self.source_website)

                # Find search field and input query
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'inline-search-input-query'))).send_keys(position)

                # Fill in localisation, confirm by choosing the option "London"
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'inline-search-input-location'))).send_keys("London")
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gc-location-autocomplete__result'))).click()
                WebDriverWait(driver, 100)
                # Confirm search
                driver.find_element(By.CLASS_NAME, "gc-inline-search__button").click()

                # Find search results on every possible page
                try:
                    while WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'gc-card'))):
                        results=driver.find_elements(By.CLASS_NAME, 'gc-card')
                        
                        # Create dictionary with job number, title and href
                        for result in results:
                            number=result.get_attribute("data-gtm-label").split("-")[0]
                            adverts[f'{number}']={'title':result.get_attribute("aria-label"),'href': result.get_attribute("href")}

                        # Go to next page
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.find_element_by_link_text('Next').click()
                except: pass               
            return adverts