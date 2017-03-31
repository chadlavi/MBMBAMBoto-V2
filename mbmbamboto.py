import os, sys
import praw
import time
import urllib
import feedparser
import re
#Special eps: The Adventure Zone:	TAZ				213
#			  Tostinos: 			Tostinos 		262
#			  Switcharoo: 			Switch 			273
episode_pattern = re.compile(r"[eE]p(?<=isode)?\ (?<=#)?(\d+)|(\!recent)|(\!TAZ)|(\!Tostino)|(\!Switch)|(\!noadvice)")
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
def get_main_list(rss_obj):
	item_lst = rss_obj["items"]
	main_ep_lst = []
	for i in item_lst:
		if len(re.findall("Me:|\d+:",i["title"])) > 0:
			main_ep_lst.append(i)
	return main_ep_lst

r = praw.Reddit('bot') # Create the reddit object
while True:
	try:
		print "Beginning of Loop"
		print(r.user.me())
		id_file = open("idfile","r+") #open the idfile
		id_file_string = id_file.read()# store the contents of idfile into a large string 
		id_file_list = id_file_string.split("\n") #split the string across newlines and store into an array
		old_len = len(id_file_list) #get the number of processed ids
		full_comments = r.subreddit('mbmbam').stream.comments() #get the comments generator
		for comment in full_comments: #for each comment in the generator
			if str(comment.id) not in id_file_list: #if thc comments id isn't in the list of processed ids; i.e. Check if the current comment has been processed or not
				id_file_list.append(str(comment.id)) #store this comments id in the list of processed ids
				print "Added " + comment.id + " to the list of processed ids"
				digit_list = [] #create a list to store the numbers found in the comment
				#comment_body_list = comment.body.split(" ")#split the body of the comment across spaces to separate it into a list of words
				reply_str = "" # prepare a string to hold the reply
				match_list = episode_pattern.findall(comment.body)
				print match_list
				for match in match_list: # for each word in the comment
					print match
					for result in match:
						if is_int(result):# if the match is a number
							digit_list.append(str(abs(int(result)))) # add the number to the list of episode numbers
						elif match=="!recent":
							feed = get_main_list(feedparser.parse("http://mbmbam.libsyn.com/rss"))
							digit_list.append(len(feed))
						elif match=="!TAZ":
							digit_list.append(-1)
						elif match=="!Switch":
							digit_list.append(-2)
						elif match=="!Tostino":
							digit_list.append(-3)
						elif match=="!noadvice":
							digit_list.append(259)

				if len(digit_list)>0: # if theres at least one link request
					feed = get_main_list(feedparser.parse("http://mbmbam.libsyn.com/rss")) # parse the rss feed
					rv_list = feed[::-1] #reverse the list of items, for easier navigation
					for ep in digit_list: # for each episode number in the comment
						if ep==-3:
							real_list=feedparser.parse("http://mbmbam.libsyn.com/rss")["items"][::-1]
							reply_str+="["+real_list[262]["title"]+"]("+real_list[262]["link"]+")\n\n  "
						elif ep==-2:
							real_list=feedparser.parse("http://mbmbam.libsyn.com/rss")["items"][::-1]
							reply_str+="["+real_list[273]["title"]+"]("+real_list[273]["link"]+")\n\n  "
						elif ep==-1:
							real_list=feedparser.parse("http://mbmbam.libsyn.com/rss")["items"][::-1]
							reply_str+="["+real_list[213]["title"]+"]("+real_list[213]["link"]+")\n\n  "
						else:
							try:
								reply_str+="[" + rv_list[abs(int(ep))-1]["title"] + "](" + rv_list[abs(int(ep))-1]["link"]+")\n\n " # try to get the ep-1th index of the list
							except IndexError: # if it doesn't exist
								reply_str+="Episode " + str(ep) + " doesn't exist!\n\n " # comment that the episode doesn't exist yet
				print reply_str	# print the full reply
				print "~~~~~~~~~~~~~\n" + comment.body + "\n~~~~~~~~~~~~~\n" #print the comment body
				if len(reply_str)>0: # if the reply string has content
					comment.reply(reply_str) #reply to the comment with the reply string
		id_file.seek(0)# go to the top of the file

		new_len = len(id_file_list) #get the length of the id list after potentially adding new ids
		if (new_len-old_len)>0: # if there are new ids, rewrite the idfile
			for id_num in id_file_list:
				id_file.write(id_num + "\n")
		id_file.close()#close the idfile
		
	except (Exception, RuntimeError) as e:
		now = time.strftime("%c")
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		err_log = open("errlog","r+")
		err_log.write("!!!\nSomething went wrong at: " + now + "\n")
		err_log.write(str(type(e)))
		err_log.write("\n!!!\n\n")
		err_log.close()
		print "something went wrong:\n", type(e),"\n",e,"\n\n",exc_type, fname, exc_tb.tb_lineno
		break
	else:
		time.sleep(5) #sleep for 5 seconds
