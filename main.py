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
        self.work()

    def work(self):
        while True:
            self.change_settings()
            self.show_settings()
            print("\nВведите 'адрес' для нового запроса")
            print("Введите 'настройки' для изменения настроек")
            print("Введите 'выход' для завершения")
            enter = input("")
            if enter == "выход":
                return
            if enter == "настройки":
                print("Изменение настроек:")
                self.settings = self.null_settings()
            if enter == "адрес":
                self.get_exact_location()
                input("Нажмите Enter")
        pass
    def get_exact_location(self):
        addres = input("Введите адрес: ")
        list_adress = get_adress(key=self.settings['key'], address=addres,language=self.settings['language'])
        if len(list_adress) > 0:
            for l in range(len(list_adress)):
                print(f"{l+1} {list_adress[l]}")

            while True:
                num_addres = input("Введите номер адреса или введите 'выйти', если нет нужного: ")
                try:
                    if num_addres == 'выйти': return
                    if num_addres == '': raise NameError("Значение не может быть пустым")
                    val = int(num_addres)
                    if val <1 or val >len(list_adress) : raise ValueError()
                    break
                except NameError as n:
                    print(n)
                except ValueError:
                    print(f"Значение может быть от 1 до {len(list_adress)}")
            result = get_coordinates(key=self.settings['key'], address=list_adress[int(num_addres)-1],language=self.settings['language'])
            print(f"Широта: {result[0]}\nДолгота: {result[1]}")

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
            print(f"Введите новое значение URL или пустую строку, чтобы установить значение {default_url}")
            url = input("URL: ")
            if url=='': url=default_url
            self.settings["url"] = url
        if self.settings.get("key") is None:
            print("\nОтсутствует API")
            while True:
                key = input("Введите новое значение ключа:")
                if key != '': break
                print("Значение не может быть пустым.")
            self.settings["key"] = key
        if self.settings.get("language") is None:
            print(f"\nВведите язык для ответа (en/ru) или пустую строку, чтобы установить значение {default_language}")
            language = input("Язык получаемых данных: ")
            if language == '': language=default_language
            if language != 'ru' and language != 'en': language=default_language
            self.settings["language"] = language
        self.dbclient.save_settings(self.settings)

if __name__ == "__main__":
    client = Client()