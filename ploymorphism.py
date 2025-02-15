class Car:
    def __init__(self,brand,model):
        self.__brand=brand
        self.model = model
    def get_brand(self):
        return self.__brand
    def fuel_type(self):
        return "petorl or disel"

class ElectricCar(Car):
    def __init__(self,brand,model,battery_size):
        super().__init__(brand, model)
        self.battery_size=battery_size
    def fuel_type(self):
        return "electric charge"
my_test=ElectricCar("telsa","s","85wkh")
print(my_test.fuel_type())

my_tata=Car("tata","safari")
print(my_tata.fuel_type())

