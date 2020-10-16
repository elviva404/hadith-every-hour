import json
from typing import Tuple


def get_hadith_track() -> Tuple[str, int]:
    with open("hadith_track.json", "r") as json_file:
        data = json.load(json_file)
        return data.get("hadith_book"), int(data.get("hadith_number"))


def update_hadith_track(hadith_book, hadith_number):
    hadith_number += 1
    with open("hadith_track.json", "w") as json_file:
        json_file.write(
            json.dumps({"hadith_book": hadith_book, "hadith_number": hadith_number})
        )
