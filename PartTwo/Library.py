from typing import List


class Item:
    def __init__(self):
        self.product_id = "product_id"
        self.quantity
        self.price = 1.0
        self.tax_bracket = 1

class Sale:
    def __init__(self, items: List[Item]):
        self.hash = "md5"
        self.timestamp = "now"
        self.subtotal = 0
        self.total = 0
        self.items = [items]

class TaxCalculator:
    def __init__(self):
        pass

    def calculateTax(self, sale: Sale) -> Sale:
        #calculate tax in the default way
        pass

class TaxCalculator2021(TaxCalculator):
    def __init__(self):
        pass

    def calculateTax(self, sale: Sale) -> Sale:
        #calculate tax in the 2021 way
        pass

class TaxCalculator2020(TaxCalculator):
    def __init__(self):
        pass

    def calculateTax(self, sale: Sale) -> Sale:
        #calculate tax in the 2020 way
        pass

class Library:
    def __init__(self, sale: Sale):
        self.sale = sale
        self.strategy = self._chooseStrategy(sale)

    def taxit(self) -> Sale:
        self.strategy.calculateTax(self.sale)

    def _chooseStrategy(self, sale: Sale) -> TaxCalculator:
        #based on some characteristic of Sale, return a specific tax calculater
        if sale.timestamp == "2021":
            return TaxCalculator2021()
        elif sale.timestamp == "2020":
            return TaxCalculator2020()
        else:
            return TaxCalculator()






