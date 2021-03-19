# Coding Test Report
In this report, I include all the code, and a sample output

## How to compile:
The command `make` runs the analysis and automatically generates this report:
 * The raw data will be downloaded and saved in feather format using `curl` and `0prepare_data.py` if it hasn't already been.
 * Then the code in `q1.py`,..., `q4.py` will be run.
 * The outputs of the code will be shown in README.md in this directory.

## Requirements
 * I'm using a MacOS 11.2.3 computer, with Xcode command line tools installed (to use `make`).
 * To install the required Python packages, run `make install_required_pip_packages`.
 * If pip isn't installed, try `make install_pip`.

## Loading data from feather file

```python
import pandas as pd
FEATHER_FILE_LOCATION = "../data/full_data_feather.feather"
df = pd.read_feather(FEATHER_FILE_LOCATION)
```



# Q1: Most expensive houses by county

```python
import pandas as pd


def get_most_expensive_houses_by_county(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the most expensive houses in each county, from the inputted pandas DataFrame
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame with highest transaction values in each county
    """
    indices_of_interest = list(df.groupby('County').max("Price")['index'])
    return df.iloc[indices_of_interest]


'''
Here is an example of this function being used:
'''
get_most_expensive_houses_by_county(df)

```

```
         index                                     UID   Price  \
672784  672784  {A71375FE-0A63-7576-E053-6C04A8C0462F}  971932
669390  669390  {BA558B32-2416-76EF-E053-6B04A8C0B4B7}  275000
673778  673778  {A71375FE-054B-7576-E053-6C04A8C0462F}  192500
673887  673887  {A71375FE-055E-7576-E053-6C04A8C0462F}   70000
674351  674351  {A71375FE-0C6D-7576-E053-6C04A8C0462F}   70000
...        ...                                     ...     ...
654312  654312  {9FF0D969-73A5-11ED-E053-6C04A8C06383}  315500
672731  672731  {A71375FE-0412-7576-E053-6C04A8C0462F}  284448
674006  674006  {A71375FE-0A35-7576-E053-6C04A8C0462F}   98000
672711  672711  {A71375FE-0CBE-7576-E053-6C04A8C0462F}   70000
672452  672452  {A71375FE-08DF-7576-E053-6C04A8C0462F}  161000

       Date_of_transfer  Postcode Property_type Old_or_new Duration  \
672784       2020-02-11   BA2 5FJ             O          Y        F
669390       2020-11-23  MK43 8QA             S          N        F
673778       2020-03-06   BB2 5NX             O          N        F
673887       2020-03-17   FY2 0HJ             T          N        F
674351       2020-02-17  NP13 3EQ             T          N        F
...                 ...       ...           ...        ...      ...
654312       2020-02-21   RG5 4HB             S          N        F
672731       2020-03-06   B98 7ST             O          N        L
674006       2020-01-24   TF4 2NQ             F          N        L
672711       2020-02-03  LL14 2DG             S          N        F
672452       2020-03-11  YO10 3SX             T          N        F

                     PAON  SAON            Street    Locality
Town_city  \
672784                  5  None   BRINKWORTH ROAD  COMBE DOWN
BATH
669390                  9  None       BERRY DRIVE     BROMHAM
BEDFORD
673778     LIVESEY CLINIC  None  CHERRY TREE LANE        None
BLACKBURN
673887          202 - 204  None     RED BANK ROAD     BISPHAM
BLACKPOOL
674351                 85  None  LANCASTER STREET      BLAINA
ABERTILLERY
...                   ...   ...               ...         ...
...
654312                 20  None     BUCKDEN CLOSE     WOODLEY
READING
672731           THE OAKS     8        CLEWS ROAD        None
REDDITCH
674006  TIMBER YARD COURT    12        HEATH HILL      DAWLEY
TELFORD
672711                 12  None     MAELOR AVENUE     PENYCAE
WREXHAM
672452                229  None       MELROSEGATE        None
YORK

                            District                        County
PPD_cat  \
672784  BATH AND NORTH EAST SOMERSET  BATH AND NORTH EAST SOMERSET
B
669390                       BEDFORD                       BEDFORD
A
673778         BLACKBURN WITH DARWEN         BLACKBURN WITH DARWEN
B
673887                     BLACKPOOL                     BLACKPOOL
B
674351                 BLAENAU GWENT                 BLAENAU GWENT
B
...                              ...                           ...
...
654312                     WOKINGHAM                     WOKINGHAM
A
672731                      REDDITCH                WORCESTERSHIRE
B
674006                        WREKIN                        WREKIN
B
672711                       WREXHAM                       WREXHAM
B
672452                          YORK                          YORK
B

       Record_status
672784             A
669390             A
673778             A
673887             A
674351             A
...              ...
654312             A
672731             A
674006             A
672711             A
672452             A

[111 rows x 17 columns]
```



# Q2: Top 5 districts by quarterly transaction value

```python
import pandas as pd


def get_districts_with_highest_transaction_values_each_quarter(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the districts with the highest transaction values in each quarter
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame with, for each quarter, the 5 districts with the highest total transaction values
    """
    # Using this guide to regex: https://stackoverflow.com/a/2013150
    df['District'] = df['Postcode'].str.extract("([^ ]*)")
    quarters_column = pd.DatetimeIndex(df['Date_of_transfer']).quarter.astype(str)
    years_column = pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str)
    df['Quarter'] = 'Q' + quarters_column + ' ' + years_column
    # How to do sorting within nested groupBy: https://stackoverflow.com/a/36074520
    return df.groupby(['Quarter', 'District']) \
        .sum('Price') \
        .sort_values(['Quarter', 'Price'], ascending=False) \
        .groupby('Quarter') \
        .head(5)


'''
Here is an example of this function being used:
'''
get_districts_with_highest_transaction_values_each_quarter(df)

```

```
                      index       Price
Quarter District
Q4 2020 W1S         2727434  1028201525
        HD8        44784096   254017354
        SW1Y        1172022   252975000
        SW19       79512192   240071406
        SW18       87650181   230170142
Q3 2020 SE1        87648664   439399692
        WC1N        3106852   298920000
        E14       115075927   273065558
        SW11       91504436   262455513
        SW6        73029481   249897010
Q2 2020 EC1V        9000247   391466450
        W2         26501448   361098515
        SW7         8686920   280847787
        E1         20064852   226693375
        W3         26630776   215770627
Q1 2020 SE1        78440132   347234209
        NW1        58794826   342127211
        SW6       109773621   315245880
        WC2A       26026314   312367110
        W2         55998451   302190911
```




# Q3: Transaction value concentration

```python
import pandas as pd


def percent_of_transactions_of_each_type_in_top_80pcnt(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gets the percent of transactions of each type which make up the top 80% of transactions by value
    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame broken down by year and property type, which shows the percentage of transactions which sum in
            value to 80% of total transaction value
    """
    df['YearAndType'] = pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str) + df['Property_type']
    transactions_summation_df = _get_80_percent_of_transaction_total_for_each_year_and_type(df)
    sorted_transactions_df = _value_of_all_sales_in_year_and_type_which_are_greater_than_this_transaction(df)
    sorted_with_category_totals_df = pd.merge(sorted_transactions_df, transactions_summation_df,
                                              on='YearAndType')
    sorted_with_category_totals_df['in_top_80%_of_value'] = sorted_with_category_totals_df['cumsum'] < \
                                                            sorted_with_category_totals_df[
                                                                '80% of Total Transaction Value']
    query_result = sorted_with_category_totals_df \
        .groupby('YearAndType') \
        .mean('in_top_80%_of_value') \
        .reset_index()[['YearAndType', 'in_top_80%_of_value']]
    query_result['Percent in top 80% of value'] = 100 * query_result['in_top_80%_of_value']
    return query_result


def _value_of_all_sales_in_year_and_type_which_are_greater_than_this_transaction(df: pd.DataFrame)->pd.DataFrame:
    """

    :param df:  a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data,
                but with a YearAndType column
    :return: DataFrame, describing for each transaction, the total value of all transactions of that year and type,
                which are greater in value to this transaction, including this transaction
    """
    sorted_transactions_df = df.sort_values(['YearAndType', 'Price'], ascending=False)
    sorted_transactions_df['cumsum'] = sorted_transactions_df.groupby('YearAndType')['Price'].transform(
        pd.Series.cumsum)
    return sorted_transactions_df


def _get_80_percent_of_transaction_total_for_each_year_and_type(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data,
                but with a YearAndType column
    :return: DataFrame, which includes the total value of each transaction type for each year, multiplied by 0.8
    """
    transactions_summation_df = df.groupby(['YearAndType']).sum('Price').reset_index().drop(['index'], axis=1)
    transactions_summation_df['Price'] = transactions_summation_df['Price'] * 0.8
    transactions_summation_df.rename(columns={'Price': '80% of Total Transaction Value'}, inplace=True)
    return transactions_summation_df


'''
Here is an example of this function being used:
'''
percent_of_transactions_of_each_type_in_top_80pcnt(df)

```

```
  YearAndType  in_top_80%_of_value  Percent in top 80% of value
0       2020D             0.620890                    62.088952
1       2020F             0.519897                    51.989695
2       2020O             0.140992                    14.099167
3       2020S             0.612286                    61.228611
4       2020T             0.541109                    54.110871
```




# Q4: Volume and median price comparisons

```python
from typing import List
import pandas as pd


def _add_price_buckets_to_df(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a pandas DataFrame, with a new (string) column, indicating which price bucket each transaction is in
    """
    cut_labels = ["£0 < x <= £250,000",
                  "£250,000 < x <= £500,000",
                  "£500,000 < x <= £750,000",
                  "£750,000 < x <= £1,000,000",
                  "£1,000,000 < x <= £2,000,000",
                  "£2,000,000 < x <= £5,000,000",
                  "£5,000,000+"]
    cut_bins = [0, 250000, 500000, 750000, 1000000, 2000000, 5000000, float("inf")]
    df['Price Bucket'] = pd.cut(df['Price'], bins=cut_bins, labels=cut_labels)
    return df


def _get_transaction_count_for_each_price_bucket(df: pd.DataFrame) -> pd.core.series.Series:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data ,
                but with a 'Price Bucket' string column added
    :return: a DataFrame describing the number of transactions in each bucket
    """
    query_result = df.groupby("Price Bucket").size()
    return query_result


def _get_median_price_for_each_bucket(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data ,
                but with a 'Price Bucket' string column added
    :return: a DataFrame describing the median transaction value for each price bucket
    """
    query_result = df.groupby("Price Bucket") \
                        .median("Price") \
                        .reset_index() \
                        .drop(['index'], axis=1) \
                        .rename(columns={'Price': 'Median Price'})
    return query_result


def __get_percentage_changes_between_two_lists(old_list: List, new_list: List) -> List[float]:
    """
    A utility function for calculating the elementwise percentage changes in values between two lists
    :param old_list: a list of floats/ints
    :param new_list: a list of the same length and types
    :return: a list of percentages, of the same length
    """
    percentage_changes_list = []
    assert (len(old_list) == len(new_list))
    for i in range(len(old_list)):
        old = old_list[i]
        new = new_list[i]
        if old==0:
            change_percent=100 #TODO: decide what to do if the number we're comparing with is 0
        else:
            change_percent = 100 * (new - old) / old
        percentage_changes_list.append(change_percent)
    return percentage_changes_list


def _get_pcnt_change_in_transaction_counts(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[float]:
    """
    Gets the percentage change in transaction counts
    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a list describing the percent differences in transaction counts in each bucket
    """
    old_transation_counts = _get_transaction_count_for_each_price_bucket(last_years_df).values
    new_transaction_counts = _get_transaction_count_for_each_price_bucket(this_years_df).values
    percentage_changes_in_transaction_count = __get_percentage_changes_between_two_lists(old_transation_counts,
                                                                                         new_transaction_counts)
    return percentage_changes_in_transaction_count


def _get_pcnt_change_in_median_prices_in_buckets(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[
    float]:
    """
    Gets the percent change in the median transaction price in each bucket
    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a list, describing the percent differences in median transaction value in each bucket
    """
    old_transaction_medians = list(_get_median_price_for_each_bucket(last_years_df)['Median Price'].values)
    new_transaction_medians = list(_get_median_price_for_each_bucket(this_years_df)['Median Price'].values)
    percentage_changes_in_medians = __get_percentage_changes_between_two_lists(old_transaction_medians,
                                                                               new_transaction_medians)
    return percentage_changes_in_medians


# %%
def compare_two_dataframes(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> pd.DataFrame:
    """

    :param last_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :param this_years_df: a pandas DataFrame like described here: https://www.gov.uk/guidance/about-the-price-paid-data
    :return: a DataFrame, which shows the percent changes in total transaction counts and median price paid,
            in each transaction bucket
    """
    cut_labels = ["£0 < x <= £250,000",
                  "£250,000 < x <= £500,000",
                  "£500,000 < x <= £750,000",
                  "£750,000 < x <= £1,000,000",
                  "£1,000,000 < x <= £2,000,000",
                  "£2,000,000 < x <= £5,000,000",
                  "£5,000,000+"]
    last_years_df = _add_price_buckets_to_df(last_years_df.copy())
    this_years_df = _add_price_buckets_to_df(this_years_df.copy())
    percent_changes_in_transaction_counts = _get_pcnt_change_in_transaction_counts(last_years_df, this_years_df)
    percent_changes_in_median_prices = _get_pcnt_change_in_median_prices_in_buckets(last_years_df, this_years_df)
    query_result = pd.DataFrame({
        "Price Buckets": cut_labels,
        "Percent change in number of transactions": percent_changes_in_transaction_counts,
        "Percent change in median prices": percent_changes_in_median_prices
    }).set_index("Price Buckets")
    return query_result


'''
Here is an example of this function being used:
'''
one_df = df.query("Town_city=='BATH'").copy()
another_df = df.query("Town_city=='BEDFORD'").copy()
compare_two_dataframes(one_df, another_df)

```

```
                              Percent change in number of transactions
\
Price Buckets
£0 < x <= £250,000                                          338.197425
£250,000 < x <= £500,000                                    149.107143
£500,000 < x <= £750,000                                      5.022831
£750,000 < x <= £1,000,000                                  -39.080460
£1,000,000 < x <= £2,000,000                                -70.329670
£2,000,000 < x <= £5,000,000                                -62.500000
£5,000,000+                                                 200.000000

                              Percent change in median prices
Price Buckets
£0 < x <= £250,000                                  -2.403846
£250,000 < x <= £500,000                            -3.579255
£500,000 < x <= £750,000                            -2.491874
£750,000 < x <= £1,000,000                          -5.747126
£1,000,000 < x <= £2,000,000                        -8.000000
£2,000,000 < x <= £5,000,000                         7.509402
£5,000,000+                                         27.210172
```


