class Task: #������� ����� "�������"

    #������� ����������� � ����������� (� ���������� ������ - protected)
    def __init__(self, time, name, url): 

        self._time = time;      
        self._name = name;
        self._url = url;

    #������� ��� ����� �������
    def get_time(self):   
        return self._time;

    def get_name(self):
        return self._name;

    def get_url(self):
        return self._url;

    # ��������������� ������ Tostring
    def __str__(self):
        text = f"- {self.get_name()} - {self.get_time()}"
        return text
    

    

    




