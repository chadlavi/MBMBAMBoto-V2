from datetime import datetime
import os, sys, praw, time, feedparser, re, logging

# SUBREDDIT-SPECIFIC VARIABLES
SUBREDDIT = 'mbmbam'

logging.basicConfig(filename='logfile', format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())

EPISODE_PATTERN = re.compile(r"[eE][pP].?\ #?(\d+)|[eE]pisode\ #?(\d+)|\!(\d+)|(\!latest)|(\!last)|(\!recent)|(![tT]roll)|([tT]rolls?\ 2)|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)")

def timestamp():
    now = datetime.now()
    return '%02d-%02d-%02d at %02d:%02d:%02d' % (now.year, now.month, now.day, now.hour, now.minute, now.second) + ' -- '

# function to get the entire list of episodes
def get_all_eps():
    feed = feedparser.parse("http://mbmbam.libsyn.com/rss")
    episodes = feed["items"]
    return list(reversed(episodes))

# function to find specific episodes based on a passed keyword, which is treated differently depending on if it is numeric or not
def get_specific_ep(keyword):
    matches_list = []
    for i in get_all_eps():
        if re.match(r"^[0-9]+$", str(keyword)):
            if re.match(r"^[1-9]$", str(keyword)):
                keyword = "0" + keyword
            if re.findall(r"[^0-9]"+str(keyword)+r"\.mp3", i["links"][1]["href"]):
                matches_list.append('[{}]({})'.format(i["title"], i["links"][1]["href"]))
        else:
            if re.findall(re.escape(str(keyword)), i["title"], re.IGNORECASE):
                matches_list.append('[{}]({})'.format(i["title"], i["links"][1]["href"]))
    return matches_list

R = praw.Reddit('bot')

logging.info("Signed in as {0}".format(str(R.user.me())))

while True:
    try:
        logging.info("Beginning to listen for new comments")
        with open('idfile', 'r+') as id_file:
            ID_FILE_STRING = id_file.read()
        ID_FILE_LIST = ID_FILE_STRING.split("\n")
        FULL_COMMENTS = R.subreddit(SUBREDDIT).stream.comments()
        for comment in FULL_COMMENTS:
            body = str(comment.body.encode('ascii', 'ignore'))
            # If the comment hasn't been checked and the author is not the bot, add the ID to the idfile and check for pattern matches in the comment body
            if str(comment.id) not in ID_FILE_LIST and str(comment.author) != 'mbmbamboto':
                with open('idfile', 'a+') as id_file:
                    # comment out the following line when debugging
                    id_file.write(str(comment.id)+"\n")
                digit_list = []
                reply_str = ""
                match_list = EPISODE_PATTERN.findall(body)
                # If there are matches, upvote the comment and find matching episode links
                if len(match_list) > 0:
                    # comment out the following line when debugging
                    comment.upvote()
                    logging.info("\n\n~~~~~~~~~~~~~\n")
                    logging.info("comment {0}: \"{1}\"".format(str(comment.id), body))
                    logging.info("comment permalink: https://www.reddit.com/r/%s%s", str(SUBREDDIT), str(comment.permalink))
                for match in match_list:
                    if type(match) == tuple:
                        for result in match:
                            if len(result) > 0:
                                for link in get_specific_ep(result):
                                    reply_str += link
                    else:
                        for link in get_specific_ep(match):
                            reply_str += link

                # If there are reply items, comment them
                if len(reply_str) > 0:
                    reply_str += "\n\n*I'm a bot. For more details see [this thread](https://www.reddit.com/r/MBMBAM/comments/62qi9c/reminder_you_can_use_the_mbmbamboto_to_quickly/).*"
                    logging.info("my reply:\n{0}".format(str(reply_str)))
                    # comment out the following line when debugging
                    comment.reply(reply_str)
                    time.sleep(5)
    except (Exception, RuntimeError) as E:
        EXC_TYPE, EXC_OBJ, EXC_TB = sys.exc_info()
        FNAME = os.path.split(EXC_TB.tb_frame.f_code.co_filename)[1]
        with open('errlog', 'a+') as err_log:
            err_log.write("Error at " + timestamp() + ":\n")
            err_log.write(str(type(E))+"\n"+str(E)+"\n"+str(EXC_TYPE)+"\nfile: "+str(FNAME)+"\nline number: "+str(EXC_TB.tb_lineno))
            err_log.write("\n\n----------\n")
        logging.error("Something went wrong:\n{}\n{}\n{}\n{}\nfile: {}\nline number: {}".format(str(timestamp()), str(type(E)), str(E), str(EXC_TYPE), str(FNAME), str(EXC_TB.tb_lineno)))
        break
