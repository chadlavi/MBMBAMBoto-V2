This is a reddit bot which will fetch links to episodes of the [My Brother, My Brother and Me](http://www.maximumfun.org/shows/my-brother-my-brother-and-me) podcast. By listening and parsing comments on the [/r/mbmbam](http://mbmbam.reddit.com) subreddit, it will comment a link to a requested episode. 

The bot listens to each comment, attempting to match the regular expression `[eE][pP].?\ #?(\d+)|[eE]pisode\ #?(\d+)|\!(\d+)|(\!latest)|(\!last)|(\!recent)|(![tT]roll)|([tT]rolls?\ 2)|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)`. For each match, it either uses the digit captured to fetch to the associated episode from the show's rss feed, or uses they keyword captured to fetch a special episode. 

**EXAMPLE**  
Say someone comments "!100". The bot matches "!100" with the regular expression, and gets the episode link for episode 100. It then processes this link into a string to comment.

**UBUNTU SETUP**  
Copy [ubuntu-setup.sh](https://bitbucket.org/chadlavimoniere/mbmbamboto-v2/raw/master/ubuntu_setup.sh) into a bash script and run it. It will prompt you for needed information, then start the script running in a new tmux session.

Attach to the session with `tmux a -t bot-running`.
