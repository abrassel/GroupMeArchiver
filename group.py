import os
from datetime import datetime
from shutil import rmtree
import urllib.request

class Group:
    def __init__(self, name, group_id):
        self.name = name
        self.group_id = group_id

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__

    def set_client(self, client):
        self.util = client.util

    def find_members(self):
        members = {user['user_id']: user['name'] for user in self.util.ask_for('/groups/'+self.group_id)['members']}
        return members


    def archive(self, foldername, target=-1):
        if os.path.exists(foldername):
            rmtree(foldername)
        os.makedirs(foldername)
        os.chdir(foldername)
        os.makedirs('logs')
        os.makedirs('images')
            
        count = 0
        self.members = self.find_members()
        prevday = None
        prevyear = None
        prevmonth = None
        curdate = open('dummy.txt','w')
        msgs = []
        for msg in self.util.get_msgs(self.group_id):
            date = msg['date']
            if date.month != prevmonth:
                if not os.path.exists("logs/%d/%d" % (date.year,date.month)):
                    os.makedirs("logs/%d/%d" % (date.year,date.month))
            if msg['date'].day != prevday:
                for message in reversed(msgs):
                    curdate.write(message)
                curdate.close()
                curdate = open('logs/%d/%d/%d.txt' % (date.year,date.month,date.day),'w')
            prevday = msg['date'].day
            prevyear = msg['date'].year
            prevmonth = msg['date'].month
            msgs.append(self.format_msg(msg)+"\n")
            for image in msg['images']:
                if not image.split('.')[-1]:
                    continue
                urllib.request.urlretrieve(image,"images/%d-%d-%d %s.%s" % (
                    msg['date'].year,
                    msg['date'].month,
                    msg['date'].day,
                    image.split('.')[-1],
                    image.split('.')[-2]))
            if count == target:
                break
            count += 1

        curdate.close()
        os.remove('dummy.txt')


    def format_msg(self, msg):
        core = "[%d:%d] %s said: '%s'" % (
            msg['date'].hour,
            msg['date'].minute,
            msg['name'],msg['text'])
        if msg['liked']:
            core += "\tLiked by: " + str(self.format_likes(msg['liked']))

        if msg['images']:
            core += " with these images attached: " + str(msg['images'])

        return core




    def format_likes(self, like_list):
        return str([self.members[person] for person in like_list if person in self.members])
            

    
