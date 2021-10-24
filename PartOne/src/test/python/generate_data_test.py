import csv
import datetime
import os
import uuid
from datetime import date

from data_generator.data_generator import DataGenerator

class TestCase:
    dirname = "src/test/resources"
    dataGenerator = DataGenerator(dirname)

    def test_generates_file(self):
        num_orders = 1000
        num_products = 10
        num_customers = 20
        self.dataGenerator.writeTables(num_orders, num_products, num_customers)
        # print(os.getcwd())
        with open(f'{self.dirname}/orders.csv') as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ['customer_id', 'product_id', 'order_date']
            rows = [row for row in reader]
            assert len(rows) == num_orders
        with open(f'{self.dirname}/products.csv') as f:
            reader = csv.DictReader(f)
            assert reader.fieldnames == ['product_id', 'product_category']
            rows = [row for row in reader]
            assert len(rows) == num_products

    def test_product_ids(self):
        fake_products = self.dataGenerator.generateProducts(self.dataGenerator.generateIds(10))
        assert len(fake_products) == 10
        uuid = fake_products[0]['product_id']
        assert self.is_valid_uuid(uuid)
        assert fake_products[0]['product_category'] in ["charms", "bracelets", "rings", "null"]

    def test_orders(self):
        expected_product_ids = ['a', 'b', 'c', 'd']
        fake_orders = self.dataGenerator.generateOrders(numOrders=10, product_ids=expected_product_ids, numCustomers=20)
        print(fake_orders)
        assert len(fake_orders) == 10

        product_id = fake_orders[0]['product_id']
        assert product_id in expected_product_ids

        order_date = date.fromisoformat(fake_orders[0]['order_date'])
        assert datetime.date(2021, 12, 31) > order_date > datetime.date(2021, 1, 1)

    def is_valid_uuid(self, uuid_to_test):
        try:
            uuid_obj = uuid.UUID(uuid_to_test)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test