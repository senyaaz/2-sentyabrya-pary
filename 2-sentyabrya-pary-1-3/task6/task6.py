class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color
    
    def info(self):
        return f"Координаты: {self.coords}, ширина: {self.width}, цвет: {self.color}"


class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length
    
    def info(self):
        return f"Линия: {super().info()}, длина: {self.length}"

class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius
    
    def info(self):
        return f"Эллипс: {super().info()}, радиус: {self.radius}"

class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height
    
    def info(self):
        return f"Прямоугольник: {super().info()}, высота: {self.height}"

line = Line((0, 0), 2, "красный", 10)
rect = Rect((5, 5), 8, "зеленый", 6)
ellipse = Ellipse((10, 10), 3, "синий", 4)

print(line.info())
print(rect.info())
print(ellipse.info())