from logging import Handler
import requests
from dataclasses import dataclass
import tweepy
import os
import json


tweet_char_limit = 260


@dataclass
class Hadith:
    _id: str
    hadith: str
    chapter: str
    narrator: str
    content: str
    hadith_number: str
    hadith_link: str = None


def make_tweet(hadith: Hadith):
    full_hadith = "\n".join([hadith.narrator, hadith.content, hadith.hadith_number])
    if len(full_hadith) > tweet_char_limit:
        link = f"\nFull hadith: {hadith.hadith_link}"
        full_hadith = full_hadith[: (tweet_char_limit - (len(link) + 3))] + "..." + link

    return full_hadith


def get_prev_word_end_index(i, full_hadith):
    while full_hadith[i] != " ":
        i -= 1
    return i


def chunk_tweet(hadith: Hadith):
    full_hadith = "\n".join([hadith.hadith_number, hadith.narrator, hadith.content])
    i = 0
    j = 0
    chunks = []
    while i < len(full_hadith):
        j += tweet_char_limit
        if j < len(full_hadith) and full_hadith[j] != " ":
            j = get_prev_word_end_index(j, full_hadith)
        chunks.append(full_hadith[i:j])
        i = j
    link = f"\nFor convenient reading: {hadith.hadith_link}"
    if len(chunks[-1]) < (tweet_char_limit - len(link)):
        chunks[-1] = chunks[-1] + link
    else:
        chunks.append(link)

    return chunks


def print_chunks(hadith: Hadith):
    for c in chunk_tweet(hadith):
        print(c)


def tweet(hadith: Hadith):
    auth = tweepy.OAuthHandler(
        os.getenv("API_KEY"),
        os.getenv("API_SECRET"),
    )
    auth.set_access_token(
        os.getenv("ACCESS_TOKEN"),
        os.getenv("ACCESS_TOKEN_SECRET"),
    )
    api = tweepy.API(auth)

    chunks = chunk_tweet(hadith)
    status = api.update_status(chunks[0])
    for i in range(1, len(chunks)):
        status = api.update_status(
            f"@HadithEveryHour {chunks[i]}", in_reply_to_status_id=status.id
        )


def tweet_hadith():

    with open("hadith_track.json", "r") as json_file:
        data = json.load(json_file)
        hadith_book = data.get("hadith_book")
        hadith_number = int(data.get("hadith_number"))

    hadith_source = "http://askhadith.herokuapp.com"
    full_hadith_source = "https://askhadith.herokuapp.com"
    hadith_link = f"{full_hadith_source}/{hadith_book}/{hadith_number}"

    resp = requests.get(f"{hadith_source}/api/{hadith_book}/{hadith_number}")
    if resp.json():
        hadith = Hadith(**resp.json())
        hadith.hadith_link = hadith_link
        print_chunks(hadith)
        # tweet(hadith)
        hadith_number += 1
        with open("hadith_track.json", "w") as json_file:
            json_file.write(
                json.dumps({"hadith_book": hadith_book, "hadith_number": hadith_number})
            )


if __name__ == "__main__":
    tweet_hadith()