from flask import jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # Add this import
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

class GetMessingInfo:
    def __init__(self, name, linkedinSector, linkedinCreatedAt, linkedinDescription , linkedinEmail, linkedinPhone):
        self.name = name
        self.linkedinSector = linkedinSector
        self.linkedinCreatedAt = linkedinCreatedAt
        self.linkedinDescription = linkedinDescription
        self.linkedinEmail = linkedinEmail
        self.linkedinPhone = linkedinPhone

    def to_dict(self):
        return {   
            "name": self.name,
            "linkedinSector": self.linkedinSector,
            "linkedinCreatedAt": self.linkedinCreatedAt,
            "linkedinDescription": self.linkedinDescription,
            "linkedinEmail": self.linkedinEmail,
            "linkedinPhone": self.linkedinPhone,
        }

    @staticmethod
    def login_LinkedIn(driver):
        try:
            driver.get("https://www.linkedin.com/login")
            username_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
            username_element.send_keys("mgrindi28@gmail.com")
            password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password")))
            password.send_keys("Izoumi123")
            btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type=submit]")))
            btn.click()

            # Wait for the homepage to load
            WebDriverWait(driver, 10).until(EC.url_contains("linkedin.com/feed"))

        except Exception as e:
            print(f"An error while login to LinkedIn: {e}")

    @staticmethod
    def complete_Info(driver):
        try:
            service = Service(executable_path="chromedriver.exe")
            driver = webdriver.Chrome(service=service)
            GetMessingInfo.login_LinkedIn(driver)
            df = pd.read_excel("startup_data.xlsx")

            for name in df['name']:
                try:
                    GetMessingInfo.shearshLinkedIn(driver, name)
                except Exception as e:
                    print(f"An error occurred while processing {name}: {e}")
                continue

            driver.quit()

        except Exception as e:
            print(f"An error occurred in complete_Info: {e}")

    @staticmethod
    def shearshLinkedIn(driver, name):
        try:
            # Preprocess company name: replace spaces with hyphens
            processed_name = name.replace(" ", "-")

            # Navigate to the company's page
            driver.get(f"https://www.linkedin.com/company/{processed_name}/about/")

            # Wait for the page to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "break-words")))

            # Fetch the HTML content of the page
            response = driver.page_source

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response, 'html.parser')

            # Find the section you want to scrape
            section = soup.find('p', class_='break-words').get_text() if soup.find('p', class_='break-words') else ""

            # Find the definition list
            dl = soup.find('dl', class_='overflow-hidden')
            if dl:
                # Extract data from the definition list
                details = {}
                for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
                    field = dt.get_text(strip=True)
                    value = dd.get_text(strip=True) if dd.get_text(strip=True) else "Not found"
                    details[field] = value

                # Add company name and section text to the data
                details['Company Name'] = name
                details['Description'] = section

                # Append data to company_data list
                company_data.append(details)

                # Increment the scrape counter
                scrape_counter += 1

                # Check if 50 scrapes have been reached
                if scrape_counter % 50 == 0:
                    print("Waiting for 1 minute...")
                    time.sleep(60)  # Wait for 1 minute
                    print("Data saved to Excel file.")

                    # Create DataFrame from company_data
                    df_company = pd.DataFrame(company_data)

                    # Ensure that the directory exists
                    os.makedirs("output_data", exist_ok=True)

                    # Save DataFrame to Excel file
                 

        except Exception as e:
            print(f"An error occurred while processing {name}: {e}")
