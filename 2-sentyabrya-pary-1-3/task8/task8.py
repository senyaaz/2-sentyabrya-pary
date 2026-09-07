class Figure:
    def __init__(self, coords, width, color):
        self.coords = coords
        self.width = width
        self.color = color
    
    def info(self):
        return f"Координаты: {self.coords}, ширина: {self.width}, цвет: {self.color}"
    
    def draw(self):
        print(f"Рисуется {self.__class__.__name__.lower()}...")


class Line(Figure):
    def __init__(self, coords, width, color, length):
        super().__init__(coords, width, color)
        self.length = length
    
    def info(self):
        return f"Линия: {super().info()}, длина: {self.length}"


class Rect(Figure):
    def __init__(self, coords, width, color, height):
        super().__init__(coords, width, color)
        self.height = height
    
    def info(self):
        return f"Прямоугольник: {super().info()}, высота: {self.height}"


class Ellipse(Figure):
    def __init__(self, coords, width, color, radius):
        super().__init__(coords, width, color)
        self.radius = radius
    
    def info(self):
        return f"Эллипс: {super().info()}, радиус: {self.radius}"


class Triangle(Figure):
    def __init__(self, coords, width, color):
        super().__init__(coords, width, color)


line = Line((0, 0), 2, "черный", 10)
rect = Rect((5, 5), 8, "синий", 6)
ellipse = Ellipse((10, 10), 3, "зеленый", 4)
triangle = Triangle((3, 3), 1, "красный")

print(line.info())
print(rect.info())
print(ellipse.info())
print(f"Треугольник: {triangle.info()}")

figures = [line, rect, ellipse, triangle]

for figure in figures:
    figure.draw()