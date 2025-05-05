# -*- coding: utf-8 -*-
from Core.Auth import AuthLMS
from Core.ParserLMS import ParserLMS
from Core.Session import SessionLMS

def main():
    session = SessionLMS(); # ������ ������

    x = ParserLMS(session); 
    arr = x.Parsing(); # ������ ������ �������� - ��������� ������� html ����� �� ������ ���� 
    task_days = x.IsExistTask(arr) # ������ ����� �������� - ����������� ���� ���

    dayWithFullTask = x.ParseDateAboutAllDay(task_days) # ������ ����� �������� - ������� � �� ������ ��������� ������� �������� Day

    for i in dayWithFullTask:
        print(i)
        print("\n-----------------\n")

main()

