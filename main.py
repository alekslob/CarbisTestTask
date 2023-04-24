from abc import ABC, abstractmethod
from typing import List, Tuple
import os
from client import Client
from api import Suggest

class Context:
    _state = None
    _client:Client

    def __init__(self, state: 'IState') -> None:
        self.set_state(state)
    
    def set_state(self, state: 'IState'):
        self._state = state
        self._state.context = self
    
    def work(self):
        self._state.work()

class IState(ABC):
    _back_state:'IState' = None

    @property
    def context(self) -> Context:
        return self._context
    
    @context.setter
    def context(self, context: Context) ->None:
        self._context = context
    
    @property
    def title(self) -> Context:
        return self._title
    
    @abstractmethod
    def work(self) ->None:
        ...

class FunctionState(IState):
    def __init__(self, title:str, back_state: IState, func = None) -> None:
        self._title = title
        self._func = func
        self._back_state = back_state

    def work(self):
        try:
            os.system('cls')
            self._func()
        finally:
            self.context.set_state(self._back_state)
            self.context.work()

class ShowCoordinates(IState):
    def __init__(self,title:str, back_state: IState, adress:Suggest):
        self._title = title
        self._adress = adress
        self._back_state = back_state
    
    def work(self) -> None:
        os.system('cls')
        print(f"Координаты адреса {self._adress.adress}:")
        print(f"{self._adress.geo_lat}: {self._adress.geo_lon}")
        input(">> ")
        self.context.set_state(self._back_state)
        self.context.work()
    
class ListAdressState(IState):
    def __init__(self,title:str, back_state: IState, list_adresses:Tuple[Suggest]):
        self._title = title
        self._list = list_adresses
        self._back_state = back_state
    def work(self) -> None:
        os.system('cls')
        for i, adress in enumerate(self._list, start=1):
            print(f"{i}. {adress.adress}")
        print(f"{i+1}. Назад")
        try:
            i = int(input(">> "))-1
            if i == len(self._list):
                self.context.set_state(self._back_state)
                self.context.work()
            elif i >= 0 and i < len(self._list):
                self.context.set_state(ShowCoordinates(title='Координаты',
                                                       back_state=self,
                                                       adress=self._list[i]))
                self.context.work()
        except ValueError:
            self.work()
        except:
            raise


class AdressState(IState):
    def __init__(self,title:str, back_state: IState, client: Client):
        self._title = title
        self._client = client
        self._back_state = back_state
    
    def work(self) -> None:
        os.system('cls')
        print("Введите адрес или пустую строку для выхода")
        try:
            suggest = input(">> ")
            if suggest == '': self.context.set_state(self._back_state)
            else: self.context.set_state(ListAdressState(title = 'Список адресов', 
                                                   back_state=self, 
                                                   list_adresses=self._client.get_adress(suggest)))
            self.context.work()
        except ValueError as e:
            self.work()
        except:
            raise

class SettingState(IState):
    def __init__(self,title:str, back_state: IState, client: Client):
        self._title = title
        self._client = client
        self._back_state = back_state
        
    @property
    def _states(self) -> List[IState]:
        return [
            FunctionState(title='Показать текущие',back_state=self, func=self._client.show_settings),
            FunctionState(title='Изменить url', back_state=self, func=self._client.change_url),
            FunctionState(title='Изменить token', back_state=self, func=self._client.change_key),
            FunctionState(title='Изменить язык', back_state=self, func=self._client.change_language),
            FunctionState(title='Назад', back_state=self._back_state)
        ]
    def work(self) -> None:
        os.system('cls')
        print(f'==={self._title}===')
        for i, state in enumerate(self._states, start=1):
            print(f"{i}. {state.title}")
        try:
            choice = int(input('>> '))
            if choice > 0 and choice <= len(self._states):
                self.context.set_state(self._states[choice-1])
                self.context.work()
            else: raise ValueError()
        except ValueError:
            self.work()
        except:
            return
        
class MainState(IState):
    def __init__(self,title:str, client:Client):
        self._title = title
        self._client = client

    @property
    def _states(self) -> List[IState]:
        return [
            AdressState(title='адрес', back_state = self, client = self._client),
            SettingState(title='настройки',back_state = self, client = self._client),
            FunctionState(title='выход', back_state=None,  func=self._client.save_changes)
        ]

    def work(self) -> None:
        os.system('cls')
        print(f'==={self._title}===')
        for i, state in enumerate(self._states, start=1):
            print(f"{i}. {state.title}")
        try:
            choice = int(input('>> '))
            if choice > 0 and choice <= len(self._states):
                self.context.set_state(self._states[choice-1])
                self.context.work()
            else: raise ValueError()
        except ValueError:
            self.work()
        except Exception as e:
            return


def get_settings():
    print('блаблабла')
    input('>> ')

if __name__ == "__main__":
    context = Context(MainState(title='Начало', client = Client()))
    context.work()