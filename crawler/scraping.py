from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

 

# URL of the page you want to scrape
url = 'https://startup.gov.tn/fr/database'

# Initialize the Edge WebDriver
driver = webdriver.Edge()

# Open the webpage
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time as needed

# Initialize a list to hold all parsed startups
all_startups = []

while True:
    # Extract the HTML content after the page has fully loaded
    html_content = driver.page_source

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table containing the startup data
    table = soup.find('table', id='startup-table')

    # Iterate over each row in the tbody of the table
    for row in table.find_all('tr'):
        # Extract data from each column in the row
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

            # Add the startup info to the list
            all_startups.append({'name': name, 'sector': sector, 'createdAt': createdAt, 'logo': image_src, 'website': website, 'label': label_data, 'description': description, 'founders': founders, 'email': email, 'phone': phone})

    # Check if there is a next page
    try:
        next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#startup-table_next')))
        if 'disabled' in next_button.get_attribute('class'):
            break  # No next page, exit the loop
        else:
            # Scroll to the next button
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)  # Adjust the sleep time as needed
            
            # Click the next page button
            next_button.click()
            time.sleep(5)  # Adjust the sleep time as needed
    except Exception as e:
        print("Error:", e)
        break

# Close the WebDriver
driver.quit()

# Print the extracted startup information
for startup in all_startups:
    print(startup)



# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(all_startups)

# Specify the path where you want to save the Excel file
excel_file_path = 'startup_data.xlsx'

# Write the DataFrame to an Excel file
df.to_excel(excel_file_path, index=False)

print("Data has been saved to:", excel_file_path)
