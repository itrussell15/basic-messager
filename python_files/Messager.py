import urllib, json, requests
import datetime
import imaplib
import email as rand
from bs4 import BeautifulSoup

class Messager:
    def __init__(self, url, email, password):
        self.url = url
        self.email = email
        self.password = password
    
    def error_handler(self, req):
        if req.status_code != 200:
            print(req.status_code)
            req.raise_for_status()
            
    def get_messages(self):
        output = requests.get(self.url)
        self.error_handler(output)
        messages = output.json()
        if len(messages) != 0:
            for mes in messages:
                mes["message_date"] = datetime.datetime.strptime(mes["message_date"][:-6], \
                     "%a, %m %b %Y %H:%M:%S")
            messages.sort(key = lambda x: x["message_date"])
            return messages
        else:
            print("No messages found")
            return None
    
    def create_message(self, payload):
        req = requests.post(self.url, json = payload)
        self.error_handler(req)
            
    def delete_message(self, _id):
        req = requests.delete(self.url + "/{}".format(_id))
        self.error_handler(req)
    
    def clear_all_messages(self):
        req = requests.delete(self.url)
        self.error_handler(req)
        print("All messages have been deleted")
    
    def mark_seen(self, _id):
        body = {"seen": True}
        req = requests.put(self.url + "/{}".format(_id), json = body)
        self.error_handler(req)
        
    def check_unread(self, server = "imap.gmail.com"):
        con = imaplib.IMAP4_SSL(server)
        con.login(self.email, self.password)
        con.select("Inbox")
        typ, data = con.search(None, "(UNSEEN)")
        msgs = []
        for num in data[0].split():
            typ, data = con.fetch(num, "(RFC822)")
            msg = rand.message_from_bytes(data[0][1])
            output = {}
            output["author"] = " ".join(msg["From"].split()[:-1])
            output["message_date"] = msg["Date"]
            soup = BeautifulSoup(msg.get_payload()[1].as_string())
            output["body"] = soup.find("body").find("div").get_text()
            typ, data = con.store(num, "-FLAGS", "//Seen")
            msgs.append(output)
        if len(msgs) == 0:
            print("No unread messages found")
            return None
        else:
            return msgs
    
    def push_new_messages(self):
        msgs = self.check_unread()
        if msgs:
            print("{} unread message(s)".format(len(msgs)))
            for m in msgs:
                self.create_message(m)
        else:
            return None
                
    def get_queued_message(self):
        msgs = self.get_messages()
        for i in msgs:
            if i["seen"] == False:
                break
        if i["seen"] == True:
            print("No messages to present")
            return None
        else:
            self.mark_seen(i["_id"])
            return i
        
    def delete_old_messages(self, thres = 5):
        cut = datetime.timedelta(hours = 1, days = thres)
        count = 0
        for msg in self.get_messages():
            diff = datetime.datetime.now() - msg["message_date"]
            if diff > cut:
                print("Message Deleted w/ Body: {}".format(msg["body"]))
                self.delete_message(msg["_id"])
                count += 1
        return count
