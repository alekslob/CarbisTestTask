from abc import ABC, abstractmethod
from typing import List
from api import APIConnect

class Context:
    _state = None

    def __init__(self, state: 'IState') -> None:
        self.set_state(state)
    
    def set_state(self, state: 'IState'):
        self._state = state
        self._state.context = self
    
    def work(self):
        self._state.work()

class IState(ABC):
    _back_state = None

    def __init__(self, title:str, states:List['IState'] = [], func = None) -> None:
        self._title = title
        self._states = states
        for state in self._states:
            state._back_state = self
        self._func = func

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
    def work(self):
        ...

class FunctionState(IState):
    def work(self):
        try:
            self._func()
        finally:
            self.context.set_state(self._back_state)
            self.context.work()
import os
class ChoiceState(IState):
    def work(self):
        os.system('cls')
        print(f'==={self._title}===')
        for i, state in enumerate(self._states, start=1):
            print(f"{i}. {state.title}")
        try:
            choice = int(input('>> '))
            if choice > 0 and choice < len(self._states):
                self.context.set_state(self._states[choice-1])
                self.context.work()
            elif choice == len(self._states):
                self.context.set_state(self._back_state)
                self.context.work()
            else: raise ValueError()
        except ValueError:
            self.work()
        except:
            return
class DataState(IState):
    def work(self):
        os.system('cls')
        print(self.title)
        try:
            adress = input(">> ")
            self._func(adress)

        except Exception as e:
            print(e)
            input(">> ")
            return
def get_settings():
    print('блаблабла')
    input('>> ')

def get_adress():
    try:
        os.system('cls')
        #обращение к бд
        api_connect = APIConnect('asd','ru')
        print('Введите адресс или 1 что бы выйти\n')
        adress = input(">> ")
        if adress != '1':
            str_choice_adress(api_connect.get_adress(adress))
            input(">> ")
    except Exception as e:
        print(e)
        input('>> ')
        # input('>> ')
        # return

def str_choice_adress(self, adresses:List) -> str:
    result = ''
    for i, adress in enumerate(adresses, start=1):
        result+=f"{i}. {adress}\n"
    return result
def str_coordinates(self, coordinates: List) -> str:
    result = f"Широта: {result[0]}\nДолгота: {result[1]}"
    return result

if __name__ == "__main__":
    
    meny = ChoiceState(title='Начало',
                       states=[FunctionState(title='адрес', func=get_adress),
                               ChoiceState(title='настройки', states=[
                                    FunctionState(title='Показать текущие', func=get_settings),
                                    FunctionState(title='Изменить url', func=get_settings),
                                    FunctionState(title='Изменить token', func=get_settings),
                                    FunctionState(title='Изменить язык', func=get_settings),
                                    FunctionState(title='Назад')
                               ]),
                               FunctionState(title='Выход')]
                       )

    
    context = Context(meny)
    context.work()