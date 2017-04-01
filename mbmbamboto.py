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
episode_pattern = re.compile(r"[eE]p.?\ #?(\d+)|[eE]pisode\ #?(\d+)|\!(\d+)|(\!latest)|(\!last)|(\!recent)|(![tT]roll)|[tT]he\ [mM]c[eE]lroy\ [bB]rothers\ [wW]ill\ [bB]e\ [iI]n\ [tT]rolls\ 2|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)")
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
	if is_int(result):# if the match is a number
		digit_list.append(str(abs(int(result)))) # add the number to the list of episode numbers
	elif result in ("!recent", "!last", "!latest"):
		feed = get_main_list(feedparser.parse("http://mbmbam.libsyn.com/rss"))
		digit_list.append(len(feed))
	elif result=="!TAZ":
		digit_list.append('taz')
	elif result=="!Switch":
		digit_list.append('switch')
	elif result=="!Tostino":
		digit_list.append('tostino')
	elif result=="!noadvice":
		digit_list.append(259)
	elif re.match('![tT]roll|[tT]he\ [mM]c[eE]lroy\ [bB]rothers\ [wW]ill\ [bB]e\ [iI]n\ [tT]rolls\ 2',result):
		digit_list.append('troll')

r = praw.Reddit('bot') # Create the reddit object
print timestamp(),'-- Signed in as ', r.user.me()
while True:
	try:
		print timestamp(),"-- Beginning to listen for new comments"
		with open("idfile", "r+") as id_file: #open the idfile
			id_file_string = id_file.read()# store the contents of idfile into a large string 
		id_file_list = id_file_string.split("\n") #split the string across newlines and store into an array
		full_comments = r.subreddit('mbmbam').stream.comments() #get the comments generator
		for comment in full_comments: #for each comment in the generator
			if str(comment.id) not in id_file_list and str(comment.author) != 'mbmbamboto': #if thc comment id isn't in the list of processed ids and comment is not by the MBMBAM bot
				#id_file_list.append(str(comment.id)) #store this comments id in the list of processed ids
				with open("idfile", "a+") as id_file: #open the idfile
					id_file.write(str(comment.id)+"\n")
				digit_list = [] #create a list to store the numbers found in the comment
				#comment_body_list = comment.body.split(" ")#split the body of the comment across spaces to separate it into a list of words
				reply_str = "" # prepare a string to hold the reply
				match_list = episode_pattern.findall(comment.body)
				if len(match_list) > 0:
					print "\n~~~~~~~~~~~~~\n"
					print "comment ",comment.id,": \n", comment.body #print the comment body
					print "comment permalink:\nhttps://www.reddit.com/r/mbmbam/", comment.permalink(fast=True)
					print "all matches from comment: ", match_list
				for match in match_list: # for each word in the comment
					print "this match: ", match
					if type(match) == tuple:
						for result in match:
							if len(result) > 0:
								print "result: ", result
								pick_ep(result)			
					else:
						pick_ep(match)
				if len(digit_list)>0: # if theres at least one link request
					rv_list = get_numbered_eps() #reverse the list of items, for easier navigation
					for ep in digit_list: # for each episode number in the comment
						print ep
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
						else:
							try:
								reply_str+="[" + rv_list[abs(int(ep))-1]["title"] + "](" + rv_list[abs(int(ep))-1]["link"]+")\n\n " # try to get the ep-1th index of the list
							except IndexError: # if it doesn't exist
								reply_str+="Episode " + str(ep) + " doesn't exist!\n\n " # comment that the episode doesn't exist yet
				if len(reply_str)>0: # if the reply string has content
					print "my reply:\n", reply_str # print the full reply
					comment.reply(reply_str) #reply to the comment with the reply string
		
	except (Exception, RuntimeError) as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		with open("errlog", "a+") as err_log:
			err_log.write("Error at " + timestamp() + ":\n")
			err_log.write(str(type(e))+"\n"+e+"\n"+exc_type+"\nfile: "+fname+"\nline number: "+exc_tb.tb_lineno)
			err_log.write("\n\n----------\n")
		print timestamp(),"-- Something went wrong:\n", type(e), "\n", e, "\n", exc_type, "\nfile: ",fname, "\nline number: ",exc_tb.tb_lineno
		break
	else:
		time.sleep(5) #sleep for 5 seconds
