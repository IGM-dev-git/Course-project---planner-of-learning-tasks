class Day:
    #Создали конструктор с параметрами (с приватными полями - protected)
    def __init__(self, theQuantityOfTask, data, arrOfTasks): 

        self._theQuantityOfTask = theQuantityOfTask;      
        self._data = data;
        self._arrOfTasks = arrOfTasks;
        

    #Сеттеры для полей объекта
    def get_theQuantityOfTask(self):   
        return self._theQuantityOfTask;

    def get_data(self):
        return self._data;

    def get_arrOfTasks(self):
        return self._arrOfTasks;

    # Переопределение метода Tostring
    def __str__(self):
        text = f"📅 {self.get_data()} - Заданий: {self.get_theQuantityOfTask()}\n\n"
        for item in self.get_arrOfTasks():
            text += f"{item}"
        return text
    




