class Car:
    def __init__(self,brand,model):
        self.__brand=brand
        self.model = model
    def get_brand(self):
        return self.__brand

class ElectricCar(Car):
    def __init__(self,brand,model,battery_size,kilometers):
        super().__init__(brand, model)
        self.battery_size=battery_size
        self.kilometers=kilometers
my_test=ElectricCar("telsa","s","85wkh","100km")
print(my_test.get_brand())