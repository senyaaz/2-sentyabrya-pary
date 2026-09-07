class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords  
        self.width = width    
        self.color = color    
    
    def info(self):
        return f"Координаты: {self.coords}, ширина: {self.width}, цвет: {self.color}"


class Circle(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius
    
    def info(self):
        return f"Круг: {super().info()}, радиус: {self.radius}"


class Rectangle(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height
    
    def info(self):
        return f"Прямоугольник: {super().info()}, высота: {self.height}"


class Triangle(Figure):
    def __init__(self, coords, width, color):
        super().__init__(coords, width, color)


circle = Circle((10, 20), 5, "красный", 3)
rect = Rectangle((0, 0), 10, "зеленый", 7)
triangle = Triangle((5, 5), 2, "синий")

print(circle.info())
print(rect.info())
print(triangle.info())