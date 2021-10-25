import csv

from faker import Faker
import numpy as np

class DataGenerator:
    def __init__(self, dirname):
        self.dirname = dirname
        self.fake = Faker()
        self.product_categories = ["charms", "bracelets", "rings", "null"]

    def generate_orders(self, num_orders, product_ids, num_customers):
        customer_ids = self.generate_ids(num_customers)
        orders = [{ 'customer_id' : np.random.choice(customer_ids), 'product_id' : np.random.choice(product_ids), 'order_date' :self.fake.date_this_year(after_today=True).isoformat()} for x in range(num_orders)]
        return orders

    def generate_products(self, productIds):
        products = [{'product_id' :x,'product_category': np.random.choice(self.product_categories, p=[0.2, 0.4, 0.3, 0.1])} for x in productIds]
        return products

    def generate_ids(self, numIds):
        return [self.fake.uuid4() for i in range(numIds)]

    def write_tables(self, num_orders, num_products, num_customers):
        productIds = self.generate_ids(num_products)
        products = self.generate_products(productIds)
        orders = self.generate_orders(num_orders, productIds, num_customers)
        self._write_table('orders', orders)
        self._write_table('products', products)

    def _write_table(self, filename, dataset):
        fieldnames = dataset[0].keys()
        with open(f'{self.dirname}/{filename}.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)