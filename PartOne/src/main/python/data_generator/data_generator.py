import csv

from faker import Faker
import numpy as np

class DataGenerator:
    def __init__(self, dirname, categories=["charms", "bracelets", "rings", "null"]):
        self.dirname = dirname
        self.fake = Faker()
        self.product_categories = categories

    def generate_orders_data(self, num_orders, product_ids, num_customers):
        customer_ids = self.generate_ids(num_customers)
        orders = [{ 'customer_id' : np.random.choice(customer_ids), 'product_id' : np.random.choice(product_ids), 'order_date' :self.fake.date_this_year(after_today=True).isoformat()} for x in range(num_orders)]
        return orders

    def generate_products_data(self, product_ids):
        products = [{'product_id' :x,'product_category': np.random.choice(self.product_categories)} for x in product_ids]
        return products

    def generate_ids(self, num_ids):
        return [self.fake.uuid4() for i in range(num_ids)]

    def write_tables(self, num_orders, num_products, num_customers):
        product_ids = self.generate_ids(num_products)
        products = self.generate_products_data(product_ids)
        orders = self.generate_orders_data(num_orders, product_ids, num_customers)
        self._write_table('orders', orders)
        self._write_table('products', products)

    def _write_table(self, filename, dataset):
        fieldnames = dataset[0].keys()
        with open(f'{self.dirname}/{filename}.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)