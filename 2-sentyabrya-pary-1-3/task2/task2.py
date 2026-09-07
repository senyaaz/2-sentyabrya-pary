class Cat:
    def __init__(self, breed, name, age):
        self.breed = breed
        self.name = name
        self.age = age
    
    def info(self):
        print(f"Порода: {self.breed}, Имя: {self.name}, Возраст: {self.age}")
    
    def draw(self):
        print(f"На экране рисуется кот {self.name}, порода {self.breed}")

cat1 = Cat("Персидская", "Снежок", 4)
cat2 = Cat("Сфинкс", "Бася", 1)
cat3 = Cat("Мейн-кун", "Оливер", 6)

cat1.info()
cat2.info()
cat3.info()

print()
      
cat1.draw()
cat2.draw()
cat3.draw()