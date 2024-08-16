from pathlib import Path
import pandas as pd
def save_dataframe_to_csv(df: pd.DataFrame, filename: str) -> None:
    output_path = Path("..")/ "data" / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    print(f"DataFrame saved to {output_path}")