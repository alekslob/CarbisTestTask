from abc import ABC, abstractmethod
from typing import List
import os
from client import Client

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
    def work(self):
        ...

class FunctionState(IState):
    def __init__(self, title:str, func = None) -> None:
        self._title = title
        self._func = func
    def work(self):
        try:
            os.system('cls')
            self._func()
        finally:
            self.context.set_state(self._back_state)
            self.context.work()

class ChoiceState(IState):
    def __init__(self, title:str, states:List['IState'] = []) -> None:
        self._title = title
        self._states = states
        for state in self._states:
            state._back_state = self
        
    def work(self):
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
        # except ValueError:
        #     self.work()
        except:
            return


def get_settings():
    print('блаблабла')
    input('>> ')

if __name__ == "__main__":
    client = Client()
    meny = ChoiceState(title='Начало',
                       states=[FunctionState(title='адрес', func=client.get_adress),
                               ChoiceState(title='настройки', states=[
                                    FunctionState(title='Показать текущие', func=client.show_settings),
                                    FunctionState(title='Изменить url', func=client.change_url),
                                    FunctionState(title='Изменить token', func=client.change_key),
                                    FunctionState(title='Изменить язык', func=client.change_language),
                                    FunctionState(title='Назад',)# lambda back_state: back_state.back_state )
                               ]),
                               FunctionState(title='Выход', func=client.save_changes)]
                       )

    
    context = Context(meny)
    context.work()