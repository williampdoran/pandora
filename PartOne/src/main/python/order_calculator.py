import pandas as pd
import numpy as np
import sys
import os
print('Python %s on %s' % (sys.version, sys.platform))
print('Path', sys.path)
print('CWD', os.getcwd())

orders_df = pd.read_csv('src/test/resources/orders.csv')
products_df = pd.read_csv('src/test/resources/products.csv')
orders_products = orders_df.merge(products_df, on='product_id').dropna()
product_categories = orders_products['product_category'].unique()


def subtract_prev_total(df, categories):
    for product_category in categories:
        df[f'prev_{product_category}_count'] = df[f'prev_{product_category}_count'] - df[f'this_order_{product_category}_count']
    return df

column_total_names = {}
aggregations = {}
for product_category in product_categories:
    orders_products[f'this_order_{product_category}_count'] = np.where(orders_products['product_category'] == product_category, 1.0, 0.0)
    aggregations[f'this_order_{product_category}_count'] = 'sum'
    column_total_names[f'this_order_{product_category}_count'] = f'prev_{product_category}_count'
    aggregations[f'prev_{product_category}_count'] = 'max'

grouped = orders_products.sort_values(by=['customer_id', 'order_date']).groupby(by=['customer_id']).expanding().sum().reset_index().set_index('level_1')
grouped.rename(columns = column_total_names, inplace=True)
total_counts = orders_products.merge(grouped, left_index=True, right_index=True)
total_counts =total_counts.groupby(by=['customer_id_x', 'order_date'], as_index=False).agg(aggregations)
final_df = subtract_prev_total(total_counts, product_categories)

with open('test.csv', 'w') as f:
    final_df.to_csv(f, index_label="order_id")

