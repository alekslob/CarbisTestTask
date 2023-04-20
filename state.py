from abc import ABC, abstractmethod
from typing import List, TypeVar,Generic
import os
T = TypeVar('T')

class Choice:
    _state = None
    _back_state = None
    _states = []

    def __init__(self, state: 'State', states: List['State']=[]) -> None:
        self.set_state(state)
        self._states = states

    @property
    def back_state(self)-> 'State':
        return self._back_state
    
    def set_state(self, state: 'State'):
        self._back_state = self._state
        self._state = state
        self._state.choice = self
    
    def work(self):
        
        new_state = self._state.work()
        # self.set_state(new_state)
        # self.work()

class State(ABC):
    def __init__(self, title:str, choices:List['State'] = []) -> None:
        self._title = title
        self._choises = choices
    
    def choises(self,choises:List['State']):
        self._choises = choises
    @property
    def choice(self) -> Choice:
        return self._choice

    @choice.setter
    def choice(self, choice: Choice) -> None:
        self._choice = choice

    @property
    def title(self):
        return self._title
    
    
    def work(self) -> 'State':
        os.system('cls')
        print(f'==={self._title}===')
        for i, choice in enumerate(self._choises, start=1):
            print(f"{i}. {choice.title}")

        try:
            chise = int(input('>> '))
            if chise > 0 and chise <= len(self._choises):
                self._choice.set_state(self._choises[chise-1])
                self._choice.work()
                # return self._choises[chise-1]
                
            else: raise ValueError()
        except:
            self.work()

class FunctionState(State):
    def __init__(self, title:str, function) -> None:
        self._title = title
        self._function = function
    
    def work(self) -> State:
        self._function()
        self._choice.back_state.work()


def get_settings():
    print('блаблабла')
    input('>> ')
    # return state.choice.back_state

# def return_state():
#     return state.choice.back_state.choice.back_state
def func_exit():
    print("Выход")
    

import sys
if __name__=="__main__":
    meny = State(title="Начало")
    adress = State(title ='адрес')
    setten = State(title='настройки',
                   choices=[
                        FunctionState('Показать текущие', get_settings),
                        FunctionState('Изменить url', get_settings),
                        FunctionState('Изменить token', get_settings),
                        FunctionState('Изменить язык', get_settings),
                        FunctionState('Выход', func_exit)
                   ])
    end = FunctionState('Выход', func_exit)
    # meny = State(title="Начало", choices=[adress,setten,end])
    meny.choises([adress,setten,end])
    choice = Choice(meny)
    choice.work()
    

    