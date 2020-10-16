from dataclasses import dataclass


@dataclass
class Hadith:
    _id: str
    hadith: str
    chapter: str
    narrator: str
    content: str
    hadith_number: str
    hadith_link: str = None
