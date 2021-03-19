from typing import List
import pandas as pd


def _add_price_buckets_to_df(df: pd.DataFrame) -> pd.DataFrame:
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
    query_result = df.groupby("Price Bucket").size()
    return query_result


def _get_median_price_for_each_bucket(df: pd.DataFrame) -> pd.DataFrame:
    query_result = df.groupby("Price Bucket").median("Price").reset_index().drop(['index'], axis=1).rename(
        columns={'Price': 'Median Price'})
    return query_result


def __get_percentage_changes_between_two_lists(old_list: List, new_list: List) -> List[float]:
    percentage_changes_list = []
    assert (len(old_list) == len(new_list))
    for i in range(len(old_list)):
        old = old_list[i]
        new = new_list[i]
        change_percent = 100 * (new - old) / old
        percentage_changes_list.append(change_percent)
    return percentage_changes_list


def _get_pcnt_change_in_transaction_counts(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[float]:
    old_transation_counts = _get_transaction_count_for_each_price_bucket(last_years_df).values
    new_transaction_counts = _get_transaction_count_for_each_price_bucket(this_years_df).values
    percentage_changes_in_transaction_count = __get_percentage_changes_between_two_lists(old_transation_counts,
                                                                                         new_transaction_counts)
    return percentage_changes_in_transaction_count


def _get_pcnt_change_in_median_prices_in_buckets(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> List[
    float]:
    old_transaction_medians = list(_get_median_price_for_each_bucket(last_years_df)['Median Price'].values)
    new_transaction_medians = list(_get_median_price_for_each_bucket(this_years_df)['Median Price'].values)
    percentage_changes_in_medians = __get_percentage_changes_between_two_lists(old_transaction_medians,
                                                                               new_transaction_medians)
    return percentage_changes_in_medians


# %%
def compare_two_dataframes(last_years_df: pd.DataFrame, this_years_df: pd.DataFrame) -> pd.DataFrame:
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


one_df = df.query("Town_city=='BATH'").copy()
another_df = df.query("Town_city=='BEDFORD'").copy()
compare_two_dataframes(one_df, another_df)
