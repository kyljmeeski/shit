from typing import List

from common import threshold, logger
from log import get_logger
from phrase import Phrase


class Conversation:
    def __init__(self, phone: str):
        self.__phone = phone
        self.__reasons = []
        self.__methods = []

    def phone(self):
        return self.__phone

    def analyze(self, text: str):
        """
        Analyzes the given phrase text, checks if it is either a REASON or a METHOD.
        :param text:
        :return:
        """
        phrase = Phrase(text)
        reasonability = phrase.reasonability()
        methodicalness = phrase.methodicalness()
        if phrase.fraudulence() < threshold:
            logger.info("Phrase is clear")
            return
        if reasonability > methodicalness:
            logger.info("Phrase is a REASON")
            self.__reasons.append(text)
        elif methodicalness > reasonability:
            logger.info("Phrase is a METHOD")
            self.__methods.append(text)

    def scam_phrases(self) -> List[str]:
        logger.debug("REASONS found : " + str(len(self.__reasons)))
        logger.debug("METHODS found : " + str(len(self.__methods)))
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
        logger.info(phone + " : " + phrase)

        conversation = self.__get_conversation(phone)
        conversation.analyze(phrase)

        scam_phrases = conversation.scam_phrases()
        if len(scam_phrases) != 0:
            self.__all.remove(conversation)
            logger.info("Conversation is fraudulence. Removed.")
        else:
            logger.info("Conversation is clear so far")

        return scam_phrases

    def __get_conversation(self, phone: str):
        """
        Returns the conversation, if there is one going.
        Otherwise, create one, add to ongoings, return it.
        :param phone: phone number of the user
        :return: conversation
        """
        for conversation in self.__all:
            if conversation.phone() == phone:
                return conversation
        else:
            conversation = Conversation(phone)
            self.__all.append(conversation)
            return conversation
