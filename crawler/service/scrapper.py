from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class Scrapper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Edge()
        self.driver.get(url)
        time.sleep(5)
        
    def scrape(self):
        all_startups = []
        while True:
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            table = soup.find('table', id='startup-table')
            for row in table.find_all('tr'):
                columns = row.find_all('td')
                if columns:
                    image_src = columns[0].find('img')['src'] if columns[0].find('img') else None
                    name = columns[1].text.strip()
                    sector = columns[2].text.strip()
                    createdAt = columns[3].text.strip()
                    label_data = columns[4].text.strip()
                    website = columns[5].find('a')['href'] if columns[5].find('a') else None
                    description = columns[6].text.strip()
                    founders = columns[7].text.strip()
                    email = columns[8].text.strip()
                    phone = columns[9].text.strip()

                    all_startups.append({'name': name, 'sector': sector, 'createdAt': createdAt, 'logo': image_src, 'website': website, 'label': label_data, 'description': description, 'founders': founders, 'email': email, 'phone': phone})

            try:
                next_button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#startup-table_next')))
                if 'disabled' in next_button.get_attribute('class'):
                    break
                else:
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                    time.sleep(1)
                    next_button.click()
            except Exception as e:
                print("Error:", e)
                break

        self.driver.quit()
        return all_startups