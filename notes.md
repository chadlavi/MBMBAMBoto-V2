* instead of using an `idfile`, maybe would be simpler to look for comments that:
    - do not have any replies by mbmbamboto
    - are from the last {{time period}}
        - maybe week? 
    - this should mean that the bot is only looking at recent comments, so that if it does manage to post some weird wrong comment, it's not on a super old comment
    - this should also mean that the bot will ignore any comment it has already replied to
* wonder how I can make it easier to gate the debug mode; currently there are 3 lines that need to be commented out to put the script in debug mode (i.e., don't post to reddit)
