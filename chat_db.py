# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 17:03:55 2017

@author: Shingi
"""

from sqlalchemy import MetaData, Table
from sqlalchemy import Integer, Column, DateTime, String
from datetime import datetime

## ** create/connect to database

metadata = MetaData('sqlite:///chat_history.sqlite')

comments_table = Table('tf_comments', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('user_input', String , nullable=False ),
                       Column('bot_response', String , nullable=False ),
                       Column('posttime', DateTime, default=datetime.now))

metadata.create_all()


# ** Database Methods
    
def upload_chat(user, botsay):
    comments_table.insert().execute(user_input=user, bot_response=botsay)
    
def delete_chat():
    print("doesn't work yet...")
    
def fetch_chats(number=0):
    results = comments_table.select().execute().fetchmany(number)
    return results
    
