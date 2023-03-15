from db import DBClient
from api import get_adress, get_coordinates
default_url = "https://dadata.ru/api/"
default_language = "ru"
default_dbname = "db.settings"

class Client:
    def __init__(self, dbname:str=default_dbname) -> None:
        print("Подключение к базе данных")
        self.dbclient = DBClient(dbname)
        print("Получение настроек")
        self.settings = self.dbclient.get_settings(self.null_settings())

    def work(self):
        while True:
            self.change_settings()
            self.show_settings()
            print("\nВведите 'адресс' для нового запроса")
            print("Введите 'настройки' для изменения настроек")
            print("Введите 'выход' для завершения")
            enter = input("")
            if enter == "выход":
                break
            if enter == "настройки":
                print("изменение настроек")
                self.settings = self.null_settings()
            if enter == "адресс":
                print("новый запрос")
                addres = input("Адресс: ")
                list_adress = get_adress(key=self.settings['key'], address=addres,language=self.settings['language'])
                if len(list_adress) > 0:
                    for l in range(len(list_adress)):
                        print(f"{l+1} {list_adress[l]}")
                    num_addres = input("Введите номер адреса или введите 'выйти', если нет нужного: ")
                    while num_addres=='':
                        print("Значение не может быть пустым.")
                        num_addres = input("Введите номер адреса или введите 'выйти', если нет нужного: ")
                    if num_addres == 'выйти':
                        continue
                    result = get_coordinates(key=self.settings['key'], address=list_adress[int(num_addres)-1],language=self.settings['language'])
                    print(f"Широта: {result[0]}\nДолгота: {result[1]}")
                input("нажмите enter")
        pass
    def show_settings(self):
        print("\nТекущие настройки:")
        print(f"URL: {self.settings['url']}")
        print(f"Ключ: {self.settings['key']}")
        print(f"Язык: {self.settings['language']}") 

    def null_settings(self):
        return {'url':None, 'key':None, 'language':None}
    def change_settings(self):
        if self.settings['url'] is None:
            print("\nОтсутствует URL")
            url = input("URL: ")
            if url=='': url=default_url
            self.settings["url"] = url
        if self.settings.get("key") is None:
            print("\nОтсутствует API")
            key = input("Ключ:")
            while key=='':
                print("пусто")
                key = input("Ключ:")
            self.settings["key"] = key
        if self.settings.get("language") is None:
            language = input("Язык: ")
            if language == '': language=default_language
            if language != 'ru' and language != 'en': language=default_language
            self.settings["language"] = language
        self.dbclient.save_settings(self.settings)

if __name__ == "__main__":
    client = Client()
    client.work()