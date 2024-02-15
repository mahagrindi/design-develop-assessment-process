from flask import jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

class StartupTunisia:
    def __init__(self, name, sector, createdAt, label, logo, website, description, founders, email, phone):
        self.name = name
        self.sector = sector
        self.created_at = createdAt
        self.label = label
        self.logo = logo
        self.website = website
        self.description = description
        self.founders = founders
        self.email = email
        self.phone = phone

    def to_dict(self):
        """Converts the Startup object into a dictionary."""
        return {
            "logo": self.logo,
            "name": self.name,
            "label": self.label,
            "sector": self.sector,
            "founders": self.founders,
            "created_at": self.created_at,
            "description": self.description,
            "website": self.website,
            "email": self.email,
            "phone": self.phone,
        }
    
    def to_extract(url):
        try:
            driver = webdriver.Edge() # Initialize the Edge WebDriver
            driver.get(url) # Open the webpage
            time.sleep(5)  # Wait for the page to load, Adjust the sleep time as needed
            all_startups = [] # Initialize a list to hold all parsed startups

            while True:
                html_content = driver.page_source # Extract the HTML content after the page has fully loaded
                soup = BeautifulSoup(html_content, 'html.parser') # Parse the HTML content with BeautifulSoup
                table = soup.find('table', id='startup-table') # Find the table containing the startup data
                for row in table.find_all('tr'): # Iterate over each row in the tbody of the table
                    columns = row.find_all('td') # Extract data from each column in the row
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

                        all_startups.append({'name': name, 'sector': sector, 'createdAt': createdAt, 'logo': image_src, 'website': website, 'label': label_data, 'description': description, 'founders': founders, 'email': email, 'phone': phone}) # Add the startup info to the list

                # Check if there is a next page
                try:
                    next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#startup-table_next')))
                    if 'disabled' in next_button.get_attribute('class'):
                        break  # No next page, exit the loop
                    else:
                        driver.execute_script("arguments[0].scrollIntoView(true);", next_button) # Scroll to the next button
                        time.sleep(1)  # Adjust the sleep time as needed
                        next_button.click() # Click the next page button
                        time.sleep(5)  # Adjust the sleep time as needed
                except Exception as e:
                    print("Error:", e)
                    break

            driver.quit()

            return jsonify({'startups': all_startups})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    

