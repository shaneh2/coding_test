import pandas as pd


def get_districts_with_highest_transaction_values_each_quarter(df: pd.DataFrame) -> pd.DataFrame:
    # Using this guide to regex: https://stackoverflow.com/a/2013150
    df['District'] = df['Postcode'].str.extract("([^ ]*)")
    df['Quarter'] = 'Q' + pd.DatetimeIndex(df['Date_of_transfer']).quarter.astype(str) \
                    + ' ' \
                    + pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str)
    # How to do sorting within nested groupBy: https://stackoverflow.com/a/36074520
    return df.groupby(['Quarter', 'District']) \
        .sum('Price') \
        .sort_values(['Quarter', 'Price'], ascending=False) \
        .groupby('Quarter') \
        .head(5)


get_districts_with_highest_transaction_values_each_quarter(df)
