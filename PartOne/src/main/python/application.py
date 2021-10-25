from data_generator.data_generator import DataGenerator
from data_generator.order_calculator import OrderCalculator

if __name__ == '__main__':
    dirname = 'output'
    dataGenerator = DataGenerator(dirname=dirname, categories=["charms", "bracelets", "rings", "necklace","null"])
    dataGenerator.write_tables(num_orders=1000, num_products=20, num_customers=20)
    output_file = f'{dirname}/aggregated_results.csv'
    OrderCalculator().generate_orders(orders_csv=f'{dirname}/orders.csv', products_csv=f'{dirname}/products.csv', output=output_file)
    print(f"Printing results to {output_file}")