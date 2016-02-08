# -*- coding: utf-8 -*-
"""
Created on Sun Jan 17 22:25:59 2016

@author: Marion
"""
import socket, time, threading
running=True
    
class Server():
    def __init__(self):
        #self.running=True?
        self.CONNECTION_LIST = []
        self.PORT =8080
        self.s = socket.socket()
        self.s.bind(("localhost", self.PORT))
        self.s.listen(5)
        self.threadnames=['t1','t2','t3','t4','t5','t6','t7']
        self.threadlist=[]        
        self.availableThread=len(self.threadlist)        
        print("server started")
        t1=threading.Thread(target=self.handleConnections).start()
        self.threadlist.append(t1)
       #_thread.start_new_thread(self.handleConnections,(self,))        
        ###get server(admin) input to help kick a player out, etc.
        
    
    def handleConnections(self):
        global running
        print('in handConnections',running)
        while running:
            print("waiting for a connection")
            c,addr=self.s.accept()
            print(type(c))
            print("connected at: ",addr)
            userName=c.recv(1024).decode('UTF-8')
            print(userName)
            user=self.User(c, addr,userName)
            user.send(("Successfully Connected").encode('utf-8'))
            #_thread.start_new_thread(self.connectionHandler,(user,))
            self.CONNECTION_LIST.append(user)
            print(self.CONNECTION_LIST)
            print('all is going well')            
            #self.CONNECTION_LIST.append(user)
            ###
            self.sendALL(user.getName()+" has connected")
            threading.Thread(target=self.connectionHandler,args=(user,)).start()
            print('in between')
            t1=threading.Thread(target=self.handleConnections).start()
            print('home run')
            
    def sendALL(self,message):
        print('sending',message)
        for user in self.CONNECTION_LIST:
            user.send(self.cleanStr((time.ctime()[12:19]+' '+message)).encode('utf-8'))
    def cleanStr(self,string):
        return string.replace("\n","")
        
    def getTime(self):
            tmpCurrTime=str(time.localtime(time.time())[3])+':'+str(time.localtime(time.time())[4])+':'+str(time.localtime(time.time())[5])
            return (str(tmpCurrTime))
    def formatMessage(self,message,user):
        msg=self.cleanStr(time.ctime()[12:19]+' '+user.getName()+':'+message)
        print(msg)        
        return msg
    def sendAll(self,username,message):
        print('sending',message)
        for user in self.CONNECTION_LIST:
            print('user',user)
            user.send(self.formatMessage(message,username).encode('utf-8'))
            
    def connectionHandler(self,user):
        print('connectionHandler')
        global running
        print(threading.active_count())
        while running:
            try:
                print('waiting on input')
                inputStr=user.conn.recv(4096).decode('UTF-8')
                print("inputstr",inputStr,type(inputStr))
                #user.setLastPost()
                
                if inputStr[0:8]==("setName"):
                    if(len(inputStr[8:])>0):
                        oldname=user.getName()
                        self.sendALL(oldname, "changed their username to ", inputStr[8:])
                    else:
                        user.conn.send(("Invalid name").encode('utf-8'))
                elif inputStr=="list":
                    user.conn.send(("Users connected: ",self.CONNECTION_LIST.values()).encode('utf-8'))
                elif inputStr=='quit':
                    user.conn.send(("Bye").encode('utf-8'))
                    user.conn.send("_")
                    user.conn.close()
                    self.sendALL(self.CONNECTION_LIST[user],"has disconnected")
                    self.CONNECTION_LIST.remove(user)
                    #kills thread                    
                    return None
                elif inputStr=='':
                    if user in self.CONNECTION_LIST.keys():
                            self.sendALL(self.CONNECTION_LIST[user],"has disconnected")
                            self.CONNECTION_LIST.remove(user)
                else:
                    self.sendAll(user,inputStr)
                    print('all good')
            except:
                if user in self.CONNECTION_LIST:
                    user.conn.close()
                    self.sendALL("User " + user.getName() + " disconnected.")
                    self.CONNECTION_LIST.remove(user)
                return None
        
        
    class User(object):

    # Each user has a Connection, Address, and a (NON-UNIQUE) username
        def __init__(self,conn, addr, name):
            self.conn = conn
            print('type of conn',type(self.conn))
            self.addr = addr
            self.name = name
            self.timeLogin = self.getTime()
            self.timeLastPost = self.getTime()
        
        def getTime(self):
            tmpCurrTime=str(time.localtime(time.time())[3])+':'+str(time.localtime(time.time())[4])+':'+str(time.localtime(time.time())[5])
            return (str(tmpCurrTime))
    
        # Function to send a message to that specific user
        def send(self, sendString):
            self.conn.send(sendString)
    
        def getName(self):
            return str(self.name)
        # Funciton to get the 'SendString' (The formatted string for when that user sent something)
        def getSendString(self, sendString):
            return ("%d:%d:%d - [" + self.name + "] > " + sendString) % (self.timeLastPost[0],self.timeLastPost[1],self.timeLastPost[2])
    
        # Self Explanitory
        def setName(self,newName):
            self.name = newName
    
        # This function returns a string that contains all the data for a specific user
        def getDataString(self):
            return ("[" + self.name + "] logged in from " + self.addr[0] + " at %d:%d:%d. Last data sent at %d:%d:%d")\
            % (self.timeLogin[0],self.timeLogin[1],self.timeLogin[2],self.timeLastPost[0],self.timeLastPost[1],self.timeLastPost[2])
    
        # This function for the '\me' command. Allows for Role Playing style of chat
        def getMeString(self, sendString):
            return ("%d:%d:%d - " + self.name + " " + sendString) % (self.timeLastPost[0],self.timeLastPost[1],self.timeLastPost[2])
    
        # This function sets the timestamp of the user's most recent comment, to see if users are active
        def setLastPost(self):
            #print "Setting Post!"
            self.timeLastPost = self.getTime()
        
                
                
Server()