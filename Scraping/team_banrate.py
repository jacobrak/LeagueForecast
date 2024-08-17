from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import os
import pandas as pd
from functions import save_dataframe_to_csv

def extract_champions_and_elements(url:str) -> pd.DataFrame:
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
def extract_teamdata(url:str) -> pd.DataFrame:
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3")
    user_data_dir = os.path.join(os.getcwd(), "chrome_user_data")
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")

    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    champions = []
    name = []
    times = []
    try:
        driver.get(url)
        containers = WebDriverWait(driver, 2).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "td.footable-visible.footable-last-column"))
    )
        

        for container in containers:
            if len(champions) >= 10:
                break
            anchor_elements = container.find_elements(By.TAG_NAME, "a")
            br_elements = container.find_elements(By.CLASS_NAME, "text-center")
            
            if anchor_elements:
                titles = [element.get_attribute("title")[:-6] for element in anchor_elements if element.get_attribute("title")]
                br = [brs.text for brs in br_elements if brs.text]

                
                champions.append(titles)
                times.append(br)
                
        
            else:
                champions.append({"titles": [], "texts": []})
        table_body = WebDriverWait(driver, 4).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > div > main > div:nth-child(7) > div > div.row.rowbreak.fond-main-cadre > div > div.row.rowbreak.pb-4 > div > table > tbody"))
        )
        
        for i in range(1, 6):
            row_selector = f"tr:nth-child({i})"
            row = table_body.find_element(By.CSS_SELECTOR, row_selector)
    
    
            cell = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)")
            anchor = cell.find_element(By.CSS_SELECTOR, "a")
            name.append(anchor.get_attribute("title")[:-6])


    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        driver.quit()
    
    flat_names = []
    flat_champions = []
    flat_times = []
    for i in range(len(name)):
        for champ, time in zip(champions[i], times[i]):
            flat_names.append(name[i])
            flat_champions.append(champ)
            flat_times.append(time)

    df = pd.DataFrame({
        "Player":flat_names,
        "Champion":flat_champions,
        "Times played":flat_times
    
    })

    return df


urls = {
    'T1': "https://gol.gg/teams/team-stats/2144/split-ALL/tournament-LCK%20Summer%202024/",
    'Dplus_KIA': "https://gol.gg/teams/team-stats/2118/split-ALL/tournament-LCK%20Summer%202024/",
    'DRX': "https://gol.gg/teams/team-stats/2119/split-ALL/tournament-LCK%20Summer%202024/",
    'FearX': "https://gol.gg/teams/team-stats/2124/split-ALL/tournament-LCK%20Summer%202024/",
    'Gen_G_eSports': "https://gol.gg/teams/team-stats/2145/split-ALL/tournament-LCK%20Summer%202024/",
    'Hanwha_Life_eSports': "https://gol.gg/teams/team-stats/2122/split-ALL/tournament-LCK%20Summer%202024/",
    'KT_Rolster': "https://gol.gg/teams/team-stats/2123/split-ALL/tournament-LCK%20Summer%202024/",
    'Kwangdong_Freecs': "https://gol.gg/teams/team-stats/2117/split-ALL/tournament-LCK%20Summer%202024/",
    'Nongshim_RedForce': "https://gol.gg/teams/team-stats/2125/split-ALL/tournament-LCK%20Summer%202024/",
    'OK_BRION': "https://gol.gg/teams/team-stats/2120/split-ALL/tournament-LCK%20Summer%202024/"
}

""""
for team_name, url in urls.items():
    
    dataframe = extract_champions_and_elements(url)
    
    filename = f"Summer_{team_name}.csv"
    save_dataframe_to_csv(dataframe, filename)
    print(f"Saved {team_name} data to {filename}")

"""


print(extract_teamdata("https://gol.gg/teams/team-stats/2144/split-ALL/tournament-LCK%20Summer%202024/"))