from Models.Day import Day


class FreeDay(Day):
    #Создали конструктор с параметрами (с приватными полями - protected)
    def __init__(self, theQuantityOfTask, data): 

        self._theQuantityOfTask = theQuantityOfTask;      
        self._data = data;

    #Сеттеры для полей объекта
    def get_theQuantityOfTask(self):   
        return self._theQuantityOfTask;

    def get_data(self):
        return self._data;

    # Переопределение метода Tostring
    def __str__(self):
        text = f"{self.get_data()} - Заданий: {self.get_theQuantityOfTask()}"
        return text
    




