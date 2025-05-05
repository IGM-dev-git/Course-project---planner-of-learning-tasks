# -*- coding: utf-8 -*-
from Core.Auth import AuthLMS
from Core.ParserLMS import ParserLMS
from Core.Session import SessionLMS

def main():
    session = SessionLMS(); # Запуск сессии

    x = ParserLMS(session); 
    arr = x.Parsing(); # Первая стадия парсинга - получения массива html кодов за каждый день 
    task_days = x.IsExistTask(arr) # Вторая часть парсинга - Определение типа дня

    dayWithFullTask = x.ParseDateAboutAllDay(task_days) # Третья часть парсинга - парсинг и на выходе получение массива объектов Day

    for i in dayWithFullTask:
        print(i)
        print("\n-----------------\n")

main()

