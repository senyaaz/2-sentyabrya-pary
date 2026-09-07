class Graph:
    def __init__(self, x=0, y=0, scale=1.0):
        self._x = x  
        self._y = y  
        self._scale = scale  
    
    def move(self, dx, dy):
        self._x += dx
        self._y += dy
        print(f"График перемещен на ({dx}, {dy})")
    
    def change_scale(self, factor):
        self._scale *= factor
        print(f"Масштаб изменен в {factor} раз")
    
    def get_state(self):
        return f"Позиция: ({self._x}, {self._y}), Масштаб: {self._scale:.1f}"
    
    def info(self):
        print(f"График: {self.get_state()}")

graph1 = Graph(0, 0, 1.0)
graph2 = Graph(5, 3, 2.0)
graph3 = Graph(-2, 4, 0.5)

print("Начальное состояние графиков:")
print("График 1:", graph1.get_state())
print("График 2:", graph2.get_state())
print("График 3:", graph3.get_state())

print("\nГрафик 1:")
graph1.move(3, -2)  
print("\nГрафик 2:")
graph2.change_scale(1.5)  

print("\nИтоговое состояние графиков")
graph1.info()
graph2.info()
graph3.info()