import json
import os
from typing import List, Dict

JSON_PATH = os.path.join("resources", "signatures.json")


def read_file() -> dict:
    with open(JSON_PATH, "r", encoding="utf") as file:
        return json.load(file)


data = read_file()


def get_base_signatures() -> List[str]:
    return data["Просьбы о переводе денег"]


def get_reason_signatures() -> Dict[str, Dict[str, List[str],]]:
    return data["Причины"]


def get_method_signatures() -> Dict[str, Dict[str, List[str]]]:
    return data["Методы"]


if __name__ == "__main__":
    print("==== REASONS ====")

    for reason, signatures in get_reason_signatures().items():
        print(reason)
        for signature in signatures:
            print("\t" + signature)
        print()

    print("==== METHODS =====")

    for method, signatures in get_method_signatures().items():
        print(method)
        for signature in signatures:
            print("\t" + signature)
        print()
