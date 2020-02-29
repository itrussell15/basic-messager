#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:10:48 2020

@author: isaactrussell
"""

import datetime
import time
import imaplib
import email as em
from bs4 import BeautifulSoup
import pandas as pd

class Messager:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.data = pd.DataFrame(columns = ["Date", "Body", "Author", "Seen"])
        
    def check_unread(self, server = "imap.gmail.com"):
        con = imaplib.IMAP4_SSL(server)
        con.login(self.email, self.password)
        con.select("Inbox")
        typ, data = con.search(None, "(UNSEEN)")
        msgs = []
        for num in data[0].split():
            typ, data = con.fetch(num, "(RFC822)")
            msg = em.message_from_bytes(data[0][1])
            output = {"Seen": False}
            output["Author"] = " ".join(msg["From"].split()[:-1])
            output["Date"] = datetime.datetime.strptime(msg["Date"], "%a, %d %b %Y %X %z")
            soup = BeautifulSoup(msg.get_payload()[1].as_string(), "lxml")
            output["Body"] = soup.find("body").find("div").get_text()
            # Tells the email that the message has been seen before.
#             typ, data = con.store(num, "-FLAGS", "//Seen") 
            msgs.append(output)
        if len(msgs) == 0:
#             print("No unread messages found")
            return None
        else:
            return msgs
        
    def messages_to_data(self):
        data = self.check_unread()
#         print(data)
        if data == None:
            print("No unread messages found")
        else:
            to_add = pd.DataFrame.from_records(data)
            self.data = self.data.append(to_add)
        return self.data
    
    unread_message_count = lambda self: (self.data["Seen"] == False).value_counts()[True]
    
    def get_queued_message(self):
        temp = self.data.sort_values(by = "Date", ascending = False)
        try:
            to_send = temp[temp["Seen"] == False].iloc[0]
            self.data.loc[self.data.Date == to_send["Date"], "Seen"] = True
            return self.data.loc[self.data.Date == to_send["Date"]]
        except:
            print("No messages to output")
        
    def check_message(self, message):
        self.data.loc[self.data.Date == message["Date"], "Seen"] = True

    def process(self):
        out = self.get_queued_message()
        print(out["Body"])
        self.check_message(out)
        
    def alert_user(self):
        print("You have {} unread messages".format(self.unread_message_count))