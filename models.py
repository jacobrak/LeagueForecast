import pandas as pd
from pathlib import Path

banrate_t1 = pd.DataFrame(pd.read_csv(Path("data") / "Summer_T1.csv"))
#banrate_t1 = pd.concat([banrate_t1.iloc[:2], banrate_t1.iloc[6:8]])

pickrate_t1 = pd.DataFrame(pd.read_csv(Path("data") / "Summer_T12.csv"))

banrate_geng = pd.DataFrame(pd.read_csv(Path("data") /"Summer_Gen_G_eSports.csv"))
pickrate_geng = pd.DataFrame(pd.read_csv(Path("data") /"Summer_Gen_G_eSports2.csv"))

best_champ = pd.DataFrame(pd.read_csv(Path("data") /"Summer_championlist.csv"))
print(banrate_t1)