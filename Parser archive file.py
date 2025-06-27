from unittest import result
from requests import Session
from bs4 import BeautifulSoup


from urllib.parse import urlparse, parse_qs 

from Models.Day import Day
from Models.FreeDay import FreeDay
from Models.Task import Task

#---------------- Начало работы с сайтом
# Заголовок имитирующий реального пользователя
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.google.com/",
}


work = Session() # Запустили сессию, с которой в дальнейшем и работаем


mainPageUrl = "https://edu.hse.ru/" #Заходим на главную страницу для получения кукки и имитации действия пользователя
work.get(mainPageUrl,headers=headers)

#---------------- Начало авторизации

authPageUrl = "https://edu.hse.ru/auth/oidckc/"  #Переходим на страницу авторизации 
response = work.get(authPageUrl,headers=headers)

#Парсим форму авторизации
soup = BeautifulSoup(response.text, 'lxml')
action = soup.find("form", id="kc-form-login").get("action")  #action это url ссылка на след этап авторизации, в данной ссылке и находятся все параемтры для словаря для пост запроса


parsed_url = urlparse(action) #Разобраться как работает эта библиотека и вся эта конструкция
query_params = parse_qs(parsed_url.query)  # Разбираем параметры запроса

# Извлекаем нужные значения
session_code = query_params.get("session_code", [""])[0] # что за синтаксис такой?
execution = query_params.get("execution", [""])[0]
client_id = query_params.get("client_id", [""])[0]
tab_id = query_params.get("tab_id", [""])[0]

print(f"session_code: {session_code}") # Проверка для себя, что параметры нашлись и все ок
print(f"execution: {execution}")
print(f"client_id: {client_id}")
print(f"tab_id: {tab_id}\n")


#создание словарика для Post запроса
data = {"session_code": session_code, "execution": execution,"client_id": client_id,"tab_id": tab_id,"username": "imgromov@edu.hse.ru","password": "HF$W1q?LYYu@","credentialId": "" }

result = work.post(action, data=data,headers=headers,allow_redirects=True) #Отправка первого пост запроса с параметрами 


soup = BeautifulSoup(result.text, 'lxml')
form = soup.find("form")

if form:
    form_action = form.get("action")
    form_data = {
        "code": form.find("input", {"name": "code"}).get("value"),
        "state": form.find("input", {"name": "state"}).get("value"),
        "session_state": form.find("input", {"name": "session_state"}).get("value")
    }
    
    # Отправляем финальный запрос
    final_response = work.post(form_action, data=form_data, headers=headers, allow_redirects=True)

#---------------- Авторизация закончена, далее возвращаемя на страницу календаря и продожаем работать с парсингом

calendar = work.get("https://edu.hse.ru/calendar/view.php?view=month",headers=headers)

soup = BeautifulSoup(calendar.text, "lxml")

info = soup.find("div",class_="calendarwrapper")
fourWeek = info.find("table")
weeks = fourWeek.find("tbody")
weeks1=weeks.find_all("tr") # Массив данных по неделям (каждый элемент массива - массив с html кодом за неделю)

all_days=[]
for week in weeks1:
    days = week.find_all("td") # Дробим на кусочки - отдельные дни
    all_days.extend(days) # Объединяя все дни в одном массиве дней (каждый элемент массива - массив с html кодом за день)

#----------------  
    
def IsExistTask(all_days=[]):
    task_days = []

    #Заполнение массива task_days значениями "Заданий нет"/"Пустой день"/"Задания есть"
    #Вторым элеметом массива второго уровня в task_days является html код
    for day in all_days:
        if 'hasevent' in (day['class']):
            task_days.append(["Задания есть",day])

        elif 'dayblank' in (day['class']):
            task_days.append(["Пустой день",day])

        else:
            task_days.append(["Заданий нет",day])

    return task_days

def ParseDateAboutAllDay(task_days = []):   
    arrayDays = [];
    for i in task_days:

        arrayTasks = []; # Массив для хранения заданий для передачи в конструктор Day()

        if i[0]=="Заданий нет":
            time = i[1].find('span', class_="sr-only").text
            arrTemp = time.split(",") #Разделили по запятой
            theNumberOfTask = arrTemp[0] #Взяли из сплит. массива данные о количестве
            dataAboutDay = arrTemp[1][1:] #Взяли из сплит. массива данные о дате дня
            
            newDay = FreeDay(theNumberOfTask,dataAboutDay); #Если в этот день ничего нет, то создается экземпляр "свободного дня" - наследника Day
            arrayDays.append(newDay);
           

        elif i[0]=="Пустой день":
            action = 0; # раз пустой день, так и не записываем ничего

        else:

            time = i[1].find('span', class_="sr-only").text # time содержит запись вида "1 событие, понедельник 12 мая"
            arrTemp = time.split(",") #Разделили по запятой

            theNumberOfTask = arrTemp[0] #Взяли из сплит. массива данные о количестве
            dataAboutDay = arrTemp[1][1:] #Взяли из сплит. массива данные о дате дня


            url = i[1].find('ul').find_all('a')
            Url = [f.get('href') for f in url if f.get('href') != '#' ]

            title = i[1].find('ul').find_all('a')
            Title = [f.get('title') for f in title if f.get('title') != None]

            for i in range(len(Url)):   #Создание массива с экземплярами заданий для передачи в конструктор Day()
                newTask = Task("18:00",Title[i],Url[i])
                arrayTasks.append(newTask)

            newDay = Day(theNumberOfTask,dataAboutDay, arrayTasks);
            arrayDays.append(newDay);


    return arrayDays

task_days = IsExistTask(all_days)

dayWithFullTask = ParseDateAboutAllDay(task_days)

for i in dayWithFullTask:
    print(i)
    print("\n-----------------\n")



