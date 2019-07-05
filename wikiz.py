# -*- coding: utf-8 -*-
"""
Reg No: R157690W
Course : CTH (Honours in Computer Science)
Search Wikipedia using the wikipedia library from http://pypi.org/wikipedia
"""
# this script module is to get information from Wikipedia (https://www.wikipedia.org)

import wikipedia

def get_wikipedia(wiki_query):
	""" gets a wikipedia entry with :
		wiki.title (Name of the wikipedia page), 
		wiki.summary (a short version of the wikipedia content),
		wiki.url (the http address where the wikipedia page can be found) and
		wiki.content (The full text entry of the wikipedia page)
	"""
	try:
		wiki = wikipedia.page(wiki_query) # search wikipedia for a page matching the input string
	except:
		wiki = None

	return wiki

## tester method
if __name__ == '__main__':
	test = input("who/what is: ")
	print("let me get that info for you...")
	info = get_wikipedia(test)
	if info is not None:
		print("url address: ", info.url)
		print("wikipedia page name: ", info.title)
		try:
			print("summary/entry: ", str(info.summary))
		except UnicodeError:
			summary = info.summary.encode("unicode-escape").decode('utf')
			print("summary/entry", summary)
	else:
		print("sorry can't find anything... pretty sure its the network")

	##  --- My FB_Messenger bot Flask app main method example ---
	# sending a wikipedia powered message:
	"""
		set_typing(sender)
		reply(sender, "let me ask uncle wikipedia...")
		set_typing(sender)
		wikipage = get_wikipedia(message)
		button_template_url(sender, wikipage.summary , wikipage.url) # post an image of what the user was looking for
		reply(sender, "there you go :-)")
	"""

## /test methods

## 