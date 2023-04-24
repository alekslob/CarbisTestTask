from dadata import Dadata
from dataclasses import dataclass
from typing import Tuple

@dataclass
class Suggest:
    adress: str
    geo_lat: str
    geo_lon: str

class APIConnect:
    def __init__(self, key:str, language:str) -> None:
        self._key = key
        self._language = language

    def get_adress(self, address:str, )->Tuple[Suggest]:
        try:
            dadata = Dadata(self._key)
            result = dadata.suggest("address", address, language=self._language)

            return [Suggest(r['unrestricted_value'], r['data']['geo_lat'], r['data']['geo_lon']) for r in result]
        except:
            raise

