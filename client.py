from db import DBClient
from api import APIConnect, Suggest
from typing import Tuple
default_dbname = "settings.db"

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

    def get_adress(self, suggest) -> Tuple[Suggest]:
        api = APIConnect(key = self._settings.key, language=self._settings.language)
        try:
            list_adresses = api.get_adress(suggest)
            if len(list_adresses) == 0:
                raise ValueError('Нет результатов по данному запросу')
            return list_adresses
        except:
            raise

    def change_url(self):
        print("Введите новый url или enther для отмены")
        try:
            url = input(">> ")
            # if url == '': raise ValueError
            if url != '':
                self._settings.url = url
        except ValueError:
            self.change_url()
            
    def change_key(self):
        print("Введите новый ключ или enther для отмены")
        try:
            key = input(">> ")
            # if key == '': raise ValueError
            if key != '':
                self._settings.key = key
        except ValueError:
            self.change_url()

    def change_language(self):
        print("Введите язык или enther для отмены")
        try:
            language = input(">> ")
            # if language == '': raise ValueError
            if language !='':
                self._settings.language = language
        except ValueError:
            self.change_url()

    def save_changes(self):
        self._dbclient.save_settings(self._settings)

if __name__ == "__main__":
    client = Client()