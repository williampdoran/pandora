import pytest
from pandas._testing import assert_frame_equal
import pandas as pd

from data_generator.order_calculator import OrderCalculator


class TestOrderCalulator:
    orderCalculator = OrderCalculator()

    def test_aggregate_orders(self):
        orders = pd.DataFrame({
            'order_date':['2021-10-24','2021-10-25','2021-10-25','2021-10-25','2021-10-26','2021-10-27'],
            'customer_id':['A','A','A','A','A','B'],
            'product_id':['P1','P2','P3','P4','P1','P3'],
            'product_category':['C1','C2','C2','C1','C1','C1']
        })
        expected_results = pd.DataFrame({
            'order_date':['2021-10-24','2021-10-25','2021-10-26','2021-10-27'],
            'customer_id':['A','A','A','B'],
            'prev_C1_count':[0.0,1.0,2.0,0.0],
            'prev_C2_count':[0.0,0.0,2.0,0.0],
            'this_order_C1_count':[1.0,1.0,1.0,1.0],
            'this_order_C2_count':[0.0,2.0,0.0,0.0]
        })
        results =self.orderCalculator.aggregate_orders(orders)
        print(results[['prev_C1_count','this_order_C1_count']])
        assert_frame_equal(results, expected_results,check_like=True)

    def test_end_to_end(self):
        self.orderCalculator.generate_orders(output='actual_output.csv')
        actual_df = pd.read_csv('actual_output.csv')
        expected_df = pd.read_csv('src/test/resources/expected_aggregated_orders.csv')
        assert_frame_equal(actual_df, expected_df,check_like=True)
