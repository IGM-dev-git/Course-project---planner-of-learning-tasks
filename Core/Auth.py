from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from Core.Session import SessionLMS

class AuthLMS:
    # Передаем в текущий класс экземпляр объекта Session с полями "заголовок" и "сессия"
    def __init__(self, currentSession):
        self.curSession = currentSession;

    def Login(self, login, password):
        authPageUrl = "https://edu.hse.ru/auth/oidckc/"  #Переходим на страницу авторизации 
        response = self.curSession.workSession.get(authPageUrl,headers=self.curSession.header)

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

        result = self.curSession.workSession.post(action, data=data,headers=self.curSession.header,allow_redirects=True) #Отправка первого пост запроса с параметрами 


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
            final_response = self.curSession.workSession.post(form_action, data=form_data, headers=self.curSession.header, allow_redirects=True)







