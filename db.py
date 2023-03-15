import sqlite3

class DBClient:
    def __init__(self, dbname:str="settings.db") -> None:
        self.connect = sqlite3.connect(dbname)
        self.cursor = self.connect.cursor()
    
    def get_settings(self, settings):
        response = self.cursor.execute("select name from sqlite_master")
        if response.fetchone() is None: return settings
        # таблицы не существует
        
        self.cursor.execute("select count(id) from settings;")
        response = self.cursor.fetchall()
        if response[0][0] == 0: return settings
        # записей не существует

        self.cursor.execute("select * from settings WHERE id=1;")
        response = self.cursor.fetchall()
        response = response[0]
        settings["url"] = response[1]
        settings["key"] = response[2]
        settings["language"] = response[3]
        return settings
    
    def save_settings(self, settings) -> None:
        url = settings.get("url")
        key = settings.get("key")
        language = settings.get("language")
        prepare_command = "create table if not exists settings (id int primary key, url varchar(255), key varchar(50), language varchar(2));"
        self.cursor.execute(prepare_command)
        command = f"insert or replace into settings (id, url, key, language) values (1, '{url}', '{key}', '{language}');"
        self.cursor.execute(command)
        self.connect.commit()

# if __name__ == '__main__':
#     dbclient = DBClient()
#     settings = {'url': 'https://dadata.ru/api/', 'key': '123', 'language': 'ru'}
#     dbclient.save_settings(settings)
#     print(dbclient.get_settings())