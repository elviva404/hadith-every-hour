<p align="center">
 <h2 align="center">Hadith Every Hour</h2>
 <p align="center">📖 A bot that Tweets a Hadith every hour</p>
 <p align="center"><i>(Every 3 hours for now to avoid spamming)</i></p>
</p>
<p align="center">
  Follow on Twitter <a href="https://twitter.com/HadithEveryHour">@HadithEveryHour</a>
</p>

### Status
Currently Tweeting the Hadiths from Sahih al-Bukhari in serial.

### Concept
It's really simple. GitHub action is written in <a href="/.github/workflows/tweet_hadith.yml">this</a> file. You can notice a scheduler - 
```
on:
  schedule:
    - cron: "0 */1 * * *"
```
And the rest of the process is self explanatory.

A tracker is used to put the latest Tweeted Hadith number in the `hadith_track.json` file. 

API's are from this project - https://github.com/Ananto30/ask-hadith

### Flow
```
Get last Tweeted Hadith number from tracker
                    ⭣
          Get Hadith from API 
                    ⭣
      Make chunks for long Hadith
                    ⭣
   Limit chunks for very long Hadith 
                    ⭣
        Tweet and comment chunks
                    ⭣
              Update tracker
```

### Contribution
There can be a different approach of Tweeting or Hadith Selection, please create an issue and let's discuss about that.
