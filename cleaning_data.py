import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape1(url)-> pd.DataFrame:
    try:
        response = requests.get(url)
        response.raise_for_status()  
    except requests.RequestException as e:
        print("Error fetching URL:", e)
        return None
    
    soup = BeautifulSoup(response.content, 'html.parser')

    tr_elements = soup.find_all('tr')

    Team_a = []
    Team_b = []
    score_a = []
    score_b = []

    for tr in tr_elements:
        td_elements = tr.find_all('td')
        if len(td_elements) >= 4:  
            Team_a.append(td_elements[1].get_text(strip=True))
            Team_b.append(td_elements[3].get_text(strip=True))
            score = td_elements[2].get_text(strip=True)
            parts = score.split(' - ')
            if len(parts) == 2:
                try: 
                    score_a.append(int(parts[0]))
                    score_b.append(int(parts[1]))
                except ValueError:
                    score_a.append(None)
                    score_b.append(None)
            else:
                score_a.append(None)
                score_b.append(None)

    df = pd.DataFrame({
        'Team A': Team_a,
        'Team B': Team_b,
        'Score A': score_a,
        'Score B': score_b,
    })
    
    return df



def scrape2(url) -> pd.DataFrame:
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
    except (requests.RequestException) as e:
        print("Error fetching URL:", e)
    
    soup = BeautifulSoup(response.content, 'html.parser')

    tr_elements = soup.find_all('tr')
    
    Champion = []
    Picks = []
    Bans = []
    Presence = []
    Wins = []
    Losses = []
    Winrate = []
    KDA = []
    Avg = []
    BT = []
    GT = []
    CSM = []
    GPM = []
    CSD = []
    GD = []
    XPD = []

    for tr in tr_elements:
        td_elements = tr.find_all('td')
        if len(td_elements) >= 15:  
            Champion.append(td_elements[0].get_text(strip=True))
            Picks.append(td_elements[1].get_text(strip=True))
            Bans.append(td_elements[2].get_text(strip=True))
            Presence.append(td_elements[3].get_text(strip=True))
            Wins.append(td_elements[4].get_text(strip=True))
            Losses.append(td_elements[5].get_text(strip=True))
            Winrate.append(td_elements[6].get_text(strip=True))
            KDA.append(td_elements[7].get_text(strip=True))
            Avg.append(td_elements[8].get_text(strip=True))
            BT.append(td_elements[9].get_text(strip=True))
            GT.append(td_elements[10].get_text(strip=True))
            CSM.append(td_elements[11].get_text(strip=True))
            GPM.append(td_elements[12].get_text(strip=True))
            CSD.append(td_elements[13].get_text(strip=True))
            GD.append(td_elements[14].get_text(strip=True))
            XPD.append(td_elements[15].get_text(strip=True))

    df = pd.DataFrame({
        'Champion': Champion,
        'Picks': Picks,
        'Bans': Bans,
        'Presence': Presence,
        'Wins': Wins,
        'Losses': Losses,
        'Winrate': Winrate,
        'KDA': KDA,
        'Avg': Avg,
        'BT': BT,
        'GT': GT,
        'CSM': CSM,
        'GPM': GPM,
        'CSD@15': CSD,
        'GD@15': GD,
        'XPD@15': XPD,
    })
    
    return df

    
#Summer_match = scrape1("https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202024/")

#Summer_championlist = scrape2("https://gol.gg/champion/list/season-S14/split-ALL/tournament-LCK%20Summer%202024/")

#Summer_T1 = scrape3("https://gol.gg/user/login/","https://gol.gg/teams/team-stats/2144/split-ALL/tournament-LCK%20Summer%202024/")

from pathlib import Path
def save_dataframe_to_csv(df: pd.DataFrame, filename: str) -> None:
    output_path = Path("data") / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"DataFrame saved to {output_path}")

#save_dataframe_to_csv(Summer_match, 'Summer_match.csv')
#save_dataframe_to_csv(Summer_championlist, 'Summer_championlist.csv')

    

""""  
Summer_T1 = scrape4("https://gol.gg/teams/team-stats/2144/split-ALL/tournament-LCK%20Summer%202024/")
Summer_Dplus_KIA = scrape4("https://gol.gg/teams/team-stats/2118/split-ALL/tournament-LCK%20Summer%202024/")
Summer_DRX = scrape4("https://gol.gg/teams/team-stats/2119/split-ALL/tournament-LCK%20Summer%202024/")
Summer_FearX = scrape4("https://gol.gg/teams/team-stats/2124/split-ALL/tournament-LCK%20Summer%202024/")
Summer_Gen_G_eSports = scrape4("https://gol.gg/teams/team-stats/2145/split-ALL/tournament-LCK%20Summer%202024/")
Summer_Hanwha_Life_eSports = scrape4("https://gol.gg/teams/team-stats/2122/split-ALL/tournament-LCK%20Summer%202024/")
Summer_KT_Rolster = scrape4("https://gol.gg/teams/team-stats/2123/split-ALL/tournament-LCK%20Summer%202024/")
Summer_Kwangdong_Freecs= scrape4("https://gol.gg/teams/team-stats/2117/split-ALL/tournament-LCK%20Summer%202024/")
Summer_Nongshim_RedForce = scrape4("https://gol.gg/teams/team-stats/2125/split-ALL/tournament-LCK%20Summer%202024/")
Summer_OK_BRION = scrape4("https://gol.gg/teams/team-stats/2120/split-ALL/tournament-LCK%20Summer%202024/")

#e = scrape4("https://gol.gg/players/player-stats/1328/season-ALL/split-ALL/tournament-LCK%20Summer%202024/")
#print(e)
print(Summer_T1)
"""
