# SUBREDDIT-SPECIFIC VARIABLES
subreddit='mbmbam'

import os, sys
import praw
import time
import urllib
import feedparser
import re
#Special eps: 	The Adventure Zone:		TAZ			213
#		Tostinos: 			Tostinos 		262
#		Switcharoo: 			Switch 			273
#		Troll:				Troll			351
episode_pattern = re.compile(r"[eE][pP].?\ #?(\d+)|[eE]pisode\ #?(\d+)|\!(\d+)|(\!latest)|(\!last)|(\!recent)|(![tT]roll)|([tT]rolls?\ 2)|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)")
def timestamp():
	return time.strftime("%c")
def is_int(n):
	try:
		int(n)
		return True
	except ValueError:
		return False

def is_empty_string(q):
	if q is "":
		return False
	else:
		return True

def get_all_eps():
	feed = feedparser.parse("http://mbmbam.libsyn.com/rss")
	item_lst = feed["items"]
	main_ep_lst = []
	for i in item_lst:
		main_ep_lst.append(i)
	return list(reversed(main_ep_lst))

def get_numbered_eps():
	item_lst = get_all_eps()
	main_ep_lst = []
	for i in item_lst:
		if len(re.findall("Me:|\d+:", i["title"])) > 0:
			main_ep_lst.append(i)
	return main_ep_lst

def pick_ep(result):
	print "result: {0}".format(str(result))
	if is_int(result):
		digit_list.append(str(abs(int(result)))) 
	elif result in ("!recent", "!last", "!latest"):
		feed = get_all_eps()
		digit_list.append('#'+str(len(feed)))
	elif result=="!TAZ":
		digit_list.append('taz')
	elif result=="!Switch":
		digit_list.append('switch')
	elif result=="!Tostino":
		digit_list.append('tostino')
	elif result=="!noadvice":
		digit_list.append(259)
	elif re.search("\!?[tT]roll", result):
		digit_list.append('troll')

r = praw.Reddit('bot') 
print "{0} -- Signed in as {1}".format(str(timestamp()), str(r.user.me()))
while True:
	try:
		print "{0} -- Beginning to listen for new comments".format(str(timestamp()))
		with open("idfile", "r+") as id_file: 
			id_file_string = id_file.read()
		id_file_list = id_file_string.split("\n") 
		full_comments = r.subreddit(subreddit).stream.comments() 
		for comment in full_comments: 
			if str(comment.id) not in id_file_list and str(comment.author) != 'mbmbamboto': 
				with open("idfile", "a+") as id_file: 
					id_file.write(str(comment.id)+"\n")
				digit_list = [] 
				reply_str = "" 
				match_list = episode_pattern.findall(comment.body)
				if len(match_list) > 0:
					print "\n~~~~~~~~~~~~~\n"
					print "comment {0}: \"{1}\"".format(str(comment.id), str(comment.body)) 
					print "comment permalink: https://www.reddit.com/r/{0}{1}".format(subreddit, str(comment.permalink(fast=True)))
					
				for match in match_list: 
					
					if type(match) == tuple:
						for result in match:
							if len(result) > 0:
								pick_ep(result)			
					else:
						pick_ep(match)
				if len(digit_list)>0: 
					rv_list = get_numbered_eps() 
					for ep in digit_list: 
						print "Matching episode: {0}".format(str(ep))
						if ep=='troll':
							real_list = get_all_eps()
							reply_str+="["+real_list[351]["title"]+"]("+real_list[351]["link"]+")\n\n  "
						elif ep=='tostino':
							real_list = get_all_eps()
							reply_str+="["+real_list[262]["title"]+"]("+real_list[262]["link"]+")\n\n  "
						elif ep=='switch':
							real_list = get_all_eps()
							reply_str+="["+real_list[273]["title"]+"]("+real_list[273]["link"]+")\n\n  "
						elif ep=='taz':
							real_list = get_all_eps()
							reply_str+="["+real_list[213]["title"]+"]("+real_list[213]["link"]+")\n\n  "
						elif re.search("#",ep):
							ep=int(ep.replace('#',''))-1
							real_list = get_all_eps()
							reply_str+="["+real_list[ep]["title"]+"]("+real_list[ep]["link"]+")\n\n  "
						else:
							try:
								reply_str+="[" + rv_list[abs(int(ep))-1]["title"] + "](" + rv_list[abs(int(ep))-1]["link"]+")\n\n " 
							except IndexError: 
								reply_str+="Episode " + str(ep) + " doesn't exist!\n\n " 
				if len(reply_str)>0: 
					reply_str+="-\n\n*I'm a bot. For more details see [this thread](https://www.reddit.com/r/MBMBAM/comments/62qi9c/reminder_you_can_use_the_mbmbamboto_to_quickly/).*"
					print "my reply:\n{0}".format(str(reply_str)) 
					comment.reply(reply_str) 
		
	except (Exception, RuntimeError) as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		with open("errlog", "a+") as err_log:
			err_log.write("Error at " + timestamp() + ":\n")
			err_log.write(str(type(e))+"\n"+str(e)+"\n"+str(exc_type)+"\nfile: "+str(fname)+"\nline number: "+str(exc_tb.tb_lineno))
			err_log.write("\n\n----------\n")
		print "{0} -- Something went wrong:\n{1}\n{2}\n{3}\nfile: {4}\nline number: {5}".format(str(timestamp()), str(type(e)), "\n", str(e), "\n", str(exc_type), "\nfile: ", str(fname), "\nline number: ", str(exc_tb.tb_lineno))
		break
	else:
		time.sleep(5) 
