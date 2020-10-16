import requests

from model import Hadith
from tracker import get_hadith_track, update_hadith_track
from twitter import tweet


def tweet_hadith():
    hadith_book, hadith_number = get_hadith_track()

    hadith_source = "http://askhadith.herokuapp.com"
    full_hadith_source = "https://askhadith.herokuapp.com"
    hadith_link = f"{full_hadith_source}/{hadith_book}/{hadith_number}"

    resp = requests.get(f"{hadith_source}/api/{hadith_book}/{hadith_number}")
    if resp.json():
        hadith = Hadith(**resp.json())
        hadith.hadith_link = hadith_link
        tweet(hadith)
        update_hadith_track(hadith_book, hadith_number)


if __name__ == "__main__":
    tweet_hadith()
