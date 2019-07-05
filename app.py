# -*- coding: utf-8 -*-
# Name      : Shamu Shingai 
# Reg Number: R157690W
# Program   : CTH
""" 
This is a prototype based on the xml retrieval based Artificial Intelligence
Markup Language (AIML) integrated with the Flask framework for web based
customer support help.

The prototype is in part for the feasibility and usability study for my 
HCT260 Major Project proposal.

For the full project i will be using the python Natural Language Toolkit and
Neural networks as they provide more capability for understanding language 
"""
import os
import random
import aiml
import sys
from flask import Flask, render_template, url_for, request, redirect
import chat_db
import wikipedia
from gtts import gTTS as gspeak


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

# Create a Kernel object to start up the chatbot 
kern = aiml.Kernel()

#load a precompiled "brain" that was created from a previous run
# This speeds up the chatbot initialisation a LOT
brainLoaded = False
forceReload = False

#creates brain if it wasn't before, otherwise loads the saved brain
while not brainLoaded: 
	if forceReload or (len(sys.argv) >= 2 and sys.argv[1] == "reload"):
		kern.bootstrap(learnFiles="std-startup.xml", commands="load aiml b")
		brainLoaded = True
		kern.saveBrain("r157690_test1.brn") #save brain for later runs
	else:
		# Attempt to load the brain file.  If it fails, fall back on the Reload
		# method.
		try:
			# The optional branFile argument specifies a brain file to load.
			kern.bootstrap(brainFile = "r157690_test1.brn")
			brainLoaded = True
		except:
			forceReload = True

kern.setBotPredicate('master', 'Shingai M Shamu')#sets AIML var </master> to me!

### The Web based component

app = Flask(__name__)

@app.route("/")
def index_page():
	return render_template("index.html") #loads the index page to interact with the bot

@app.route("/chat") #Chat interface logic
def chat_page():
	if( request.args.get("question") is not None):
		user_query = request.args.get("question")
		chat_reply = kern.respond(user_query)
		chat_db.upload_chat(user_query,chat_reply)
	else: 
		chat_reply = "Hello.how may i help you?"
	return render_template("chat.html", chatbot_say=chat_reply)

@app.route("/voice") #Chat interface logic
def voice_chat():
	if( request.args.get("question") is not None):
		user_query = request.args.get("question")
		if 'who is' in user_query.lower():
			vquery = user_query.lower().strip('who is')
			wikipedia_info = get_wikipedia(vquery)
			if wikipedia_info is not None:
				chat_reply = wikipedia_info.summary[:1000]+"..."
		else:
			chat_reply = kern.respond(user_query)
			chat_db.upload_chat(user_query,chat_reply)
	else:
		user_query = ''
		chat_reply = "Hello how may i help you?"
	try:
		os.remove('/static/reply.mp3')
	except OSError:
		pass
	chat_voice = gspeak(chat_reply[:200])
	chat_voice.save("static/reply.mp3")
	return render_template("voice.html", chatbot_say=chat_reply, user_said=user_query)

@app.route("/chathistory")
def check_data():
	history = chat_db.fetch_chats()
	return render_template("history.html", chats=history)

if __name__ == "__main__":
	app.run(debug=True)