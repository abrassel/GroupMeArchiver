#!/usr/bin/python3

import pyAesCrypt
import zipfile
import os
from client import Client

def archive(c=None):
    if not c:
        oauth = input('''To continue, please enter your GroupMe authentication token.
    If you need help finding it, please go to https://dev.groupme.com/ and log-in.

Token: ''')


        c = Client(oauth)
    search = input("Great! Now, please enter a name to search for: ")
    g = None
    for group_list in c.search_groups_by_name(search):
        for (i,group) in enumerate(group_list):
            print("%d) %s" % (i+1, group.name))
        if len(group_list) == 10:
            print("0) Next groups")
        isFirst = True
        choice = 'oops'
        while not choice.isdigit() or int(choice) > 9:
            if not isFirst:
                print("Invalid selection.")
            isFirst = False
            choice = input("Enter selection #: ")

        os.system("clear")
        if choice != '0':
            g = group_list[int(choice)-1]
            break
    
    if not g:
        print("No more groups.  Restarting...")
        archive(c)

    g.set_client(c)

    firstTime = True
    choice = 'oops'
    while not (choice.isdigit() or choice == 'all'):
        if not firstTime:
            print("That was an invalid selection.")
            firstTime = False
        choice = input("Great!  Now, how many messages would you like to pull? Enter 'all' if you just want everything in this group chat.\n\nEnter here: ").strip().lower()

    destination = input("\n\nFinally, I need you to tell me what folder to put these images in. please enter the path to your new folder here.  Be careful!! This program will delete the folder you name if it currently exists.\n\nEnter destination here: ")

    if choice == 'all':
        choice = -1
    else:
        choice = int(choice)
    g.archive(destination, choice)
    
    
def encrypt(): 
    archive = ""
    first = True
    while not os.path.exists(archive):
        if not first:
            print("You did not provide a valid archive name.")
        first = False
        archive = input("Please provide the path for the target archive: ")

        
    password = input("Great!  Now please provide the password you would like to use to AES encrypt your archive: ")

    compressed_name = archive + ".zip"

    with zipfile.ZipFile(compressed_name, 'w') as myfile:
        print("{} has been created!".format(compressed_name))
        myfile.write(archive)

    # encryption/decryption buffer size - 64K
    bufferSize = 64 * 1024

    # encrypt
    pyAesCrypt.encryptFile(compressed_name, archive + ".aes", password, bufferSize)
    print("{} has been created!".format(archive + ".aes"))
   
 

action = None
first = True

options = {'1': archive,
           '2': encrypt
           }

while action not in options:
    if not first:
        print("Option: %s is an invalid selection" % (action,))
    first = False
    action = input('''Welcome! What would you like to do today?
    1) Archive a GroupMe chat.
    2) Compress and encrypt an archived chat.

Enter your response (1 or 2) here: ''')
os.system('clear')

options[action]()
    


    
    
