import pandas as pd
import numpy as np
import sys
import os
print('Python %s on %s' % (sys.version, sys.platform))
print('Path', sys.path)
print('CWD', os.getcwd())


class OrderCalculator:

    def _read_data_files(self, orders_csv, products_csv):
        orders_df = pd.read_csv(orders_csv)
        products_df = pd.read_csv(products_csv)
        return orders_df.merge(products_df, on='product_id').dropna()

    def _subtract_prev_total(self, df, categories):
        for category in categories:
            df[f'prev_{category}_count'] = df[f'prev_{category}_count'] - df[f'this_order_{category}_count']
            df.rename(columns={'customer_id_x':'customer_id'}, inplace=True)
        return df

    def _get_cols_to_rename(self, categories):
        return {f'this_order_{category}_count': f'prev_{category}_count' for category in categories}

    def _get_col_aggregations(self, categories):
        aggs = {}
        for category in categories:
            aggs[f'this_order_{category}_count'] = 'sum'
            aggs[f'prev_{category}_count'] = 'max'
        return aggs


    def _set_initial_category_count(self, df, categories):
        for category in categories:
            df[f'this_order_{category}_count'] = np.where(df['product_category'] == category, 1.0, 0.0)
        return df

    def _group_order_counts(self, df, rename):
        grouped = df.sort_values(by=['customer_id', 'order_date']).groupby(
            by=['customer_id']).expanding().sum().reset_index().set_index('level_1')
        grouped.rename(columns=rename, inplace=True)
        return df.merge(grouped, left_index=True, right_index=True)

    def _write_output(self, filename, df):
        with open(filename, 'w') as f:
            df.to_csv(f, index_label="order_id")

    def aggregate_orders(self, orders_products_data):
        product_categories = orders_products_data['product_category'].unique()
        cols_to_rename = self._get_cols_to_rename(product_categories)
        aggregations = self._get_col_aggregations(product_categories)

        orders_products_with_counts = self._set_initial_category_count(orders_products_data, product_categories)
        total_counts = self._group_order_counts(orders_products_with_counts, cols_to_rename)
        orders_agg_by_customer_date = total_counts.groupby(by=['customer_id_x', 'order_date'], as_index=False).agg(
            aggregations)
        return self._subtract_prev_total(orders_agg_by_customer_date, product_categories)

    def generate_orders(self, orders_csv='src/test/resources/orders.csv', products_csv='src/test/resources/products.csv',
                        output='test.csv'):
        orders_products = self._read_data_files(orders_csv, products_csv)
        final_df = self.aggregate_orders(orders_products)
        self._write_output(output, final_df)

OrderCalculator().generate_orders()