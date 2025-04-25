import math
from enum import Enum
from queue import Queue

class Roles(Enum):
    USER = 0
    MODEL = 1

MAX_TOKENS = 4096 * 2

class ContextWindow:
    def __init__(self, max_size:int=128, max_tokens:int=4096):
        self.max_tokens = max_tokens
        self.__history = []
        self.max_tokens = max_tokens
        
        self.system_prompt = {"role": Roles.MODEL, "content": ''}
        self.user_prompt = {"role": Roles.USER, "content": ''}
    
    #legacy
    def _add_message_context(self, message:str, text:str):
        message['context'] = text.split()
        self.__history.append((message, message.split()))

    def add_system_message(self, text:str) -> None:
        self.system_prompt['context'] = text.split()
        self.__history.append(self.system_prompt)

    def add_user_message(self, text:str) -> None:
        self.user_prompt['context'] = text.split()
        self.__history.append(self.user_prompt)

    def count_tokens(self) -> int:
        counter:int = 0
        for x in self.__history:
            counter += len(x['context'])
        return counter
    
    def count_conversation_length(self):
        return len(self.__history)
    
    def get_history(self) -> None:
        return self.__history
