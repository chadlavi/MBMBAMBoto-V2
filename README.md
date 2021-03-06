# MBMBAMBOTO V2 #

This is a reddit bot which will fetch links to episodes of the [My Brother, My Brother and Me](http://www.maximumfun.org/shows/my-brother-my-brother-and-me) podcast. By listening and parsing comments on the [/r/mbmbam](http://mbmbam.reddit.com) subreddit, it will comment a link to a requested episode. 

The bot listens to each comment, attempting to match the regular expression `[eE][pP].?\ #?(\d+)|[eE]pisode\ #?(\d+)|\!(\d+)|(\!latest)|(\!last)|(\!recent)|(![tT]roll)|([tT]rolls?\ 2)|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)`. For each match, it either uses the digit captured to fetch to the associated episode from the show's rss feed, or uses they keyword captured to fetch a special episode. 

Note that you'll need these pieces of info to set up the required `praw.ini` file:

* your script's client id 
* your script's client secret 
* your bot user's username 
* your bot user's password 
* a string to provide for your bot's user agent (NOTE: Reddit requires that the string follow the format `[script name] by [user]`, if you don't follow this format you'll get 403 errors from PRAW)

You can see an example of the required `praw.ini` file in the `example_praw.ini` file.

## NOTES
See [notes](notes.md) for TODOs and current design thinking on the bot.

## THANKS!  
This is based on an original version of the bot written by Reddit user [/u/Quip_Qwop](https://bitbucket.org/Quip_Qwop/), which I updated to work with newer versions of PRAW (now compatible with [praw 5.2.0](http://praw.readthedocs.io/en/v5.2.0/)) and removed some secrets from, so it could be public.

