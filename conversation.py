from typing import List

from common import threshold
from phrase import Phrase


class Conversation:
    def __init__(self, phone: str):
        self.__phone = phone
        self.__reasons = []
        self.__methods = []

    def phone(self):
        return self.__phone

    def add(self, text: str):
        phrase = Phrase(text)
        reasonability = phrase.reasonability()
        methodicalness = phrase.methodicalness()
        if phrase.fraudulence() < threshold:
            return
        if reasonability > methodicalness:
            self.__reasons.append(text)
        elif methodicalness > reasonability:
            self.__methods.append(text)

    def scam_phrases(self) -> List[str]:
        if len(self.__reasons) > 0 and len(self.__methods) > 0:
            return self.__reasons + self.__methods
        return []

    def __eq__(self, other):
        if isinstance(other, Conversation):
            return self.phone() == other.phone()
        return False


class Conversations:
    def __init__(self):
        self.__all = []

    def analyze(self, phone: str, phrase: str) -> List[str]:
        for item in self.__all:
            if item.phone() == phone:
                conversation = item
                break
        else:
            conversation = Conversation(phone)
            self.__all.append(conversation)

        conversation.add(phrase)

        scam_phrases = conversation.scam_phrases()
        if len(scam_phrases) != 0:
            self.__all.remove(conversation)

        return scam_phrases
