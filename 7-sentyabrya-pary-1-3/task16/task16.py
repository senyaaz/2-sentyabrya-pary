import random

class Line:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Rect:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)

class Ellipse:
    def __init__(self, a, b, c, d):
        self.sp = (a, b)
        self.ep = (c, d)
        
elements = []

for _ in range(217):
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    c = random.randint(0, 100)
    d = random.randint(0, 100)
    
    class_choice = random.choice([Line, Rect, Ellipse])
    elements.append(class_choice(a, b, c, d))

for obj in elements:
    if isinstance(obj, Line):
        obj.sp = (0, 0)
        obj.ep = (0, 0)