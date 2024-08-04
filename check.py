from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
import pandas as pd
from cleaning_data import save_dataframe_to_csv
def extract_champions_and_elements(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    champions = []
    content = ""
    try:
        driver.get(url)
        container = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > main > div:nth-child(7) > div > div.row.rowbreak.fond-main-cadre > div > div:nth-child(2)"))
        )
        anchor_elements = container.find_elements(By.TAG_NAME, "a")
        champions = [element.get_attribute("title")[:-6] for element in anchor_elements if element.get_attribute("title")]

        elements = WebDriverWait(driver, 2).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "nostyle"))
        )
        for element in elements:
            content +=  element.text

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
    
    pattern = r'(\d+)%'


    matches = re.findall(pattern, content)

    percentages = [float(match) / 100 for match in matches]

    df = pd.DataFrame({
    'Champion_a': champions[:5],
    'Overall Ban Rate (%)': percentages[:5],
    'Champion_b': champions[5:10],
    'Blueside Ban Rate (%)': percentages[5:10],
    'Champion_c': champions[10:15],
    'Redside Ban Rate (%)': percentages[10:15],
    'Champion_d': champions[15:20],
    'Overall Ban Rate Against (%)': percentages[15:20],
    'Champion_e': champions[20:25],
    'Blueside Ban Rate Against (%)': percentages[20:25],
    'Champion_f': champions[25:30],
    'Redside Ban Rate Against (%)': percentages[25:30]
})


    return df

# Example usage
url1 = "https://gol.gg/teams/team-stats/2144/split-ALL/tournament-LCK%20Summer%202024/"


data = extract_champions_and_elements(url1)
print(data)



