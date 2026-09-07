class Car:
    def __init__(self):
        self._engine_temperature = 20  
    
    def start_engine(self):
        self._engine_temperature = 90
        print("Двигатель прогрет")
    
    def drive(self):
        if self._engine_temperature >= 90:
            print("Поехали")
        else:
            print("Двигатель не прогрет, сначала запустите start_engine()")

my_car = Car()

print(f"Проверка на доступ к _engine_temperature: {my_car._engine_temperature}°C")
print("Попытка поехать без прогрева:")
my_car.drive()  

print("\nПрогреваем двигатель")
my_car.start_engine()  
print(f"Температура после прогрева: {my_car._engine_temperature}°C")
my_car.drive()  