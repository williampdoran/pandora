import pandas as pd
import numpy as np
import sys
import os
print('Python %s on %s' % (sys.version, sys.platform))
print('Path', sys.path)
print('CWD', os.getcwd())


def read_data_files(orders_csv, products_csv):
    orders_df = pd.read_csv(orders_csv)
    products_df = pd.read_csv(products_csv)
    return orders_df.merge(products_df, on='product_id').dropna()


def set_initial_category_count(df, categories):
    for category in categories:
        df[f'this_order_{category}_count'] = np.where(df['product_category'] == category, 1.0, 0.0)
    return df


def subtract_prev_total(df, categories):
    for category in categories:
        df[f'prev_{category}_count'] = df[f'prev_{category}_count'] - df[f'this_order_{category}_count']
        df.rename(columns={'customer_id_x':'customer_id'}, inplace=True)
    return df


def get_cols_to_rename(categories):
    return {f'this_order_{category}_count': f'prev_{category}_count' for category in categories}


def get_col_aggregations(categories):
    aggs = {}
    for category in categories:
        aggs[f'this_order_{category}_count'] = 'sum'
        aggs[f'prev_{category}_count'] = 'max'
    return aggs


def group_order_counts(df, rename):
    grouped = df.sort_values(by=['customer_id', 'order_date']).groupby(
        by=['customer_id']).expanding().sum().reset_index().set_index('level_1')
    grouped.rename(columns=rename, inplace=True)
    return df.merge(grouped, left_index=True, right_index=True)


def write_output(filename, df):
    with open(filename, 'w') as f:
        df.to_csv(f, index_label="order_id")


def aggregate_orders(orders_products_data):
    product_categories = orders_products_data['product_category'].unique()
    cols_to_rename = get_cols_to_rename(product_categories)
    aggregations = get_col_aggregations(product_categories)

    orders_products_with_counts = set_initial_category_count(orders_products_data, product_categories)
    total_counts = group_order_counts(orders_products_with_counts, cols_to_rename)
    orders_agg_by_customer_date = total_counts.groupby(by=['customer_id_x', 'order_date'], as_index=False).agg(
        aggregations)
    return subtract_prev_total(orders_agg_by_customer_date, product_categories)


def generate_orders(orders_csv='src/test/resources/orders.csv', products_csv='src/test/resources/products.csv',
                    output='test.csv'):
    orders_products = read_data_files(orders_csv, products_csv)
    final_df = aggregate_orders(orders_products)
    write_output(output, final_df)

