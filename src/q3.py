import pandas as pd


def percent_of_transactions_of_each_type_in_top_80pcnt(df: pd.DataFrame) -> pd.DataFrame:
    df['YearAndType'] = pd.DatetimeIndex(df['Date_of_transfer']).year.astype(str) + df['Property_type']
    transactions_summation_df = df.groupby(['YearAndType']).sum('Price').reset_index().drop(['index'], axis=1)
    transactions_summation_df['Price'] = transactions_summation_df['Price'] * 0.8
    transactions_summation_df.rename(columns={'Price': '80% of Total Transaction Value'}, inplace=True)
    sorted_transactions_df = df.sort_values(['YearAndType', 'Price'], ascending=False)
    sorted_transactions_df['cumsum'] = sorted_transactions_df.groupby('YearAndType')['Price'].transform(
        pd.Series.cumsum)
    sorted_transactions_with_category_totals = pd.merge(sorted_transactions_df, transactions_summation_df,
                                                        on='YearAndType')
    sorted_transactions_with_category_totals['in_top_80%_of_value'] = sorted_transactions_with_category_totals[
                                                                          'cumsum'] < \
                                                                      sorted_transactions_with_category_totals[
                                                                          '80% of Total Transaction Value']
    query_result = \
    sorted_transactions_with_category_totals.groupby('YearAndType').mean('in_top_80%_of_value').reset_index()[
        ['YearAndType', 'in_top_80%_of_value']]
    query_result['Percent in top 80% of value'] = 100 * query_result['in_top_80%_of_value']
    return query_result


percent_of_transactions_of_each_type_in_top_80pcnt(df)
