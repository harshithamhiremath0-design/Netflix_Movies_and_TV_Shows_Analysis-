import pandas as pd

def load_data(file):

    df = pd.read_csv(file)

    df.columns = df.columns.str.strip()

    df.fillna("Unknown", inplace=True)

    return df
