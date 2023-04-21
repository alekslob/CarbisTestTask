from dadata import Dadata
from dataclasses import dataclass
from typing import List

@dataclass
class APIData:
    url: str = "https://dadata.ru/api/"
    key: str = ''
    language: str = 'ru'

class APIConnect:
    def __init__(self, key:str, language:str) -> None:
        self._key = key
        self._language = language
    def get_adress(self, address:str, )->list:
        try:
            dadata = Dadata(self._key)
            result = dadata.suggest("address", address, language=self._language)
            result = [r['unrestricted_value'] for r in result]
            return result
        except:
            raise

    def get_coordinates(self, address:str)->list:
        try:
            dadata = Dadata(self._key)
            result = dadata.suggest("address", address, language=self._language,count=1)
            result=result[0]
            return [result['data']['geo_lat'], result['data']['geo_lon']]
        except:
            raise
