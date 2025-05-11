import spacy

from common import threshold, logger
from setup import MODEL_PATH
from signatures import get_reason_signatures, get_method_signatures

nlp = spacy.load(MODEL_PATH)


def compare(left: str, right: str) -> float:
    return nlp(left).similarity(nlp(right))


class Phrase:
    def __init__(self, text: str):
        self.__text = text

    def reasonability(self) -> float:
        for reason, signatures in get_reason_signatures().items():
            max_similarity = -1
            best_hit = ""

            for signature in signatures:
                similarity = compare(self.__text, signature)
                logger.debug(signature + " : " + str(similarity))
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_hit = signature

            if max_similarity >= threshold:
                return max_similarity

        return 0.0

    def methodicalness(self) -> float:
        for method, signatures in get_method_signatures().items():
            max_similarity = -1
            best_hit = ""

            for signature in signatures:
                similarity = compare(self.__text, signature)
                logger.debug(signature + " : " + str(similarity))
                if similarity > max_similarity:
                    max_similarity = similarity
                    best_hit = signature

            if max_similarity >= threshold:
                return max_similarity

        return 0.0

    def fraudulence(self) -> float:
        return max(self.reasonability(), self.methodicalness())


if __name__ == "__main__":
    # phrase = Phrase("здравствуйте")
    # print(phrase.methodicalness())
    # print(compare("здравстуйте", "назовите ваш паспортный номер"))
    # print(compare("здравствуйте", "назовите ваш паспортный номер"))
    print(compare("здравстуйте", "здравстуйте"))
