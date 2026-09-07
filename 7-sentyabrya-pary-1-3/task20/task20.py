class Cart:
    def __init__(self):
        self.goods = []
    
    def add(self, gd):
        self.goods.append(gd)
    
    def remove(self, indx):
        if 0 <= indx < len(self.goods):
            del self.goods[indx]
    
    def get_list(self):
        return [f'{item.name}: {item.price}' for item in self.goods]


class Table:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class TV:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Notebook:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Cup:
    def __init__(self, name, price):
        self.name = name
        self.price = price

cart = Cart()

cart.add(TV('Samsung', 92000))
cart.add(TV('LG', 67000))
cart.add(Table('Круглый стол', 4000))
cart.add(Notebook('MSI', 90000))
cart.add(Notebook('HP', 35000))
cart.add(Cup('стеклянная кружка', 340))