# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from Core.Auth import AuthLMS
from Models.Day import Day
from Models.FreeDay import FreeDay
from Models.Task import Task
from Sqlite import *

class ParserLMS:

    login = Database.GetAllUserData()['login']
    password = Database.GetAllUserData()['password']
     
    def __init__(self, currentSession, chat_id):
        self.curSession = currentSession;
        self.chat_id = chat_id;

    # Метод для получения массива с html кодом каждого дня текущего месяца (элементами массива явзяются неразобранные блоки html кода каждого дня)
    def Parsing (self):

        mainPageUrl = "https://edu.hse.ru/"; #Заходим на главную страницу для получения кукки и имитации действия пользователя
        self.curSession.workSession.get(mainPageUrl,headers=self.curSession.header);

        login = AuthLMS(self.curSession)
        login.Login(self.login,self.password)

        calendar = self.curSession.workSession.get("https://edu.hse.ru/calendar/view.php?view=month",headers=self.curSession.header)

        soup = BeautifulSoup(calendar.text, "lxml")

        info = soup.find("div",class_="calendarwrapper")
        fourWeek = info.find("table")
        weeks = fourWeek.find("tbody")
        htmlCodeOfWeeks=weeks.find_all("tr") # Массив данных по неделям (каждый элемент массива - массив с html кодом за неделю)

        htmlCodeOfAllDays=[]
        for week in htmlCodeOfWeeks:
            days = week.find_all("td") # Дробим на кусочки - отдельные дни
            htmlCodeOfAllDays.extend(days) # Объединяя все дни в одном массиве дней (каждый элемент массива - массив с html кодом за день)

        return htmlCodeOfAllDays;

    # Метод для определения типа дней. Возвращает массив в котором хранятся пары ["тип дня", код дня]
    def IsExistTask(self,all_days=[]):
        task_days = []

        #Заполнение массива task_days значениями "Заданий нет"/"Пустой день"/"Задания есть"
        #Вторым элеметом массива второго уровня в task_days является html код дня 
        for day in all_days:
            if 'hasevent' in (day['class']):
                task_days.append(["Задания есть",day])

            elif 'dayblank' in (day['class']):
                task_days.append(["Пустой день",day]) # Пустой день, день не существующий в текущем месяце

            else:
                task_days.append(["Заданий нет",day]) # День, когда нет каких-либо заданий 

        return task_days

    # Метод создания массива из элементов типа Day и наследуемого класса (Возвращает массив элементами типа Day)
    def ParseDateAboutAllDay(self,task_days = []):   
        arrayDays = [];
        for i in task_days:

            arrayTasks = []; # Массив для хранения заданий для передачи в конструктор Day()

            if i[0]=="Заданий нет":
                time = i[1].find('span', class_="sr-only").text
                arrTemp = time.split(",") #Разделили по запятой
                theNumberOfTask = arrTemp[0] #Взяли из сплит. массива данные о количестве
                dataAboutDay = arrTemp[1][1:] #Взяли из сплит. массива данные о дате дня
                dataAboutDay = dataAboutDay[0].upper() + dataAboutDay[1:]
            
                newDay = FreeDay(theNumberOfTask,dataAboutDay); #Если в этот день ничего нет, то создается экземпляр "свободного дня" - наследника Day
                arrayDays.append(newDay);
           

            elif i[0]=="Пустой день":
                action = 0; # раз пустой день, так и не записываем ничего

            else:

                time = i[1].find('span', class_="sr-only").text # time содержит запись вида "1 событие, понедельник 12 мая"
                arrTemp = time.split(",") #Разделили по запятой

                theNumberOfTask = arrTemp[0] #Взяли из сплит. массива данные о количестве
                dataAboutDay = arrTemp[1][1:] #Взяли из сплит. массива данные о дате дня
                dataAboutDay = dataAboutDay[0].upper() + dataAboutDay[1:]

                # Получение персональной ссылки события
                url = i[1].find('ul').find_all('a')
                Url = [f.get('href') for f in url if f.get('href') != '#' ]

                # Получение названия события
                title = i[1].find('ul').find_all('a')
                Title = [f.get('title') for f in title if f.get('title') != None]

                for i in range(len(Url)):   #Создание массива с экземплярами заданий для передачи в конструктор Day()
                    
                    # Получаем даты завершения задания по персональной ссылке экземпляра
                    completionTimeGet = self.curSession.workSession.get(Url[i],headers=self.curSession.header)
                    completionTimeText = BeautifulSoup(completionTimeGet.text, "lxml")
                    # При разборе данной строки парсится не те данные, которые можно увидеть в коде
                    completionTime = (completionTimeText.find("div",class_="activity-information").find("div",class_="description-inner").text).split(",")[-1]
                    

                    newTask = Task(completionTime,Title[i],Url[i])
                    arrayTasks.append(newTask)
                    
                
                newDay = Day(theNumberOfTask,dataAboutDay, arrayTasks);
                arrayDays.append(newDay);


        return arrayDays




