from db import DBClient
# from api import get_adress, get_coordinates
# default_url = "https://dadata.ru/api/"
# default_language = "ru"
default_dbname = "db.settings"

class Client:
    def __init__(self, dbname:str=default_dbname) -> None:
        print("Подключение к базе данных")
        self._dbclient = DBClient(dbname)
        print("Получение настроек")
        self._settings = self._dbclient.get_settings()

    def show_settings(self):
        print("Текущие настройки\n")
        print(f"{self._settings.url}:{self._settings.key} {self._settings.language}")
        input(">> ")

    def change_url(self):
        print("Введите новый url или 0 для отмены")
        try:
            url = input(">> ")
            if url == '': raise ValueError
            if url != '0':
                self._settings.url = url
        except ValueError:
            self.change_url()
            
    def change_key(self):
        print("Введите новый ключ или 0 для отмены")
        try:
            key = input(">> ")
            if key == '': raise ValueError
            if key != '0':
                self._settings.key = key
        except ValueError:
            self.change_url()
            
    def change_language(self):
        print("Введите язык или 0 для отмены")
        try:
            language = input(">> ")
            if language == '': raise ValueError
            if language !='0':
                self._settings.language = language
        except ValueError:
            self.change_url()

    def save_changes(self):
        self._dbclient.save_settings(self._settings)

if __name__ == "__main__":
    client = Client()