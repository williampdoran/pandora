import csv

from faker import Faker
import numpy as np

class DataGenerator:
    def __init__(self, dirname):
        self.dirname = dirname
        self.fake = Faker()
        self.product_categories = ["charms", "bracelets", "rings", "null"]

    def generateOrders(self, numOrders, product_ids, numCustomers):
        customerIds = self.generateIds(numCustomers)
        orders = [{'customer_id' : np.random.choice(customerIds), 'product_id' : np.random.choice(product_ids), 'order_date' :self.fake.date_this_year(after_today=True).isoformat()} for x in range(numOrders)]
        return orders

    def generateProducts(self, productIds):
        products = [{'product_id' :x,'product_category': np.random.choice(self.product_categories, p=[0.2, 0.4, 0.3, 0.1])} for x in productIds]
        return products

    def generateIds(self, numIds):
        return [self.fake.uuid4() for i in range(numIds)]

    def writeTables(self, numOrders, numProducts, numCustomers):
        productIds = self.generateIds(numProducts)
        products = self.generateProducts(productIds)
        orders = self.generateOrders(numOrders, productIds, numCustomers)
        self._writeTable('orders', orders)
        self._writeTable('products', products)

    def _writeTable(self, filename, dataset):
        fieldnames = dataset[0].keys()
        with open(f'{self.dirname}/{filename}.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(dataset)