class Figure:
    def __init__(self, x, y):
        self.__x = x      
        self.__y = y
    
    def get_coords(self):
        return (self.__x, self.__y)
    
    def set_coords(self, x, y):
        self.__x = x
        self.__y = y


class Circle(Figure):
    def __init__(self, x, y, r):
        super().__init__(x, y)
        self.r = r
    
    def calculate_area(self):
        return 3.14 * self.r * self.r  
class Square(Figure):
    def __init__(self, x, y, side):
        super().__init__(x, y)
        self.side = side
    
    def calculate_area(self):
        return self.side * self.side

figures = [
    Circle(0, 0, 5),
    Square(10, 10, 4),
    Circle(3, 5, 2.5),
    Square(20, 15, 6),
    Circle(-5, 3, 3.2)
]

total = 0
for f in figures:
    total += f.calculate_area()

print("Общая площадь:", round(total, 2))