import pandas as pd


def get_most_expensive_houses_by_county(df: pd.DataFrame) -> pd.DataFrame:
    indices_of_interest = list(df.groupby('County').max("Price")['index'])
    return df.iloc[indices_of_interest]


get_most_expensive_houses_by_county(df)
