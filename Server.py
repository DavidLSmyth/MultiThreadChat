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
        #connectionList holds a list of users that have connected
        self.connectionList = []
        self.PORT =8080
        self.s = socket.socket()
        self.s.bind(("localhost", self.PORT))
        #at most 5 people can join the chat
        self.s.listen(5)
        self.threadlist=[]        
        self.availableThread=len(self.threadlist)        
        print("server started")
        self.threadlist.append(threading.Thread(target=self.handleNewConnections).start())
       #_thread.start_new_thread(self.handleNewConnections,(self,))        
        ###get server(admin) input to help kick a player out, etc.
        
    
    def handleNewConnections(self):
        '''Waits for an incoming connection and then deals with connecting the user'''
        global running
        print('in handConnections',running)
        while running:
            print("waiting for a connection")
            c,addr=self.s.accept()
            userName=c.recv(1024).decode('UTF-8')
            print(userName,"connected at: ",addr)
            user=self.User(c, addr,userName)
            #user.send(("Successfully Connected").encode('utf-8'))
            #_thread.start_new_thread(self.connectionHandler,(user,))
            self.connectionList.append(user)
            print(self.connectionList)      
            #Let eveyone know that the user has connected
            self.sendALL(user.getName()+" has connected")
            #deal with the current connection
            threading.Thread(target=self.connectionHandler,args=(user,)).start()
            #wait for a new connection
            threading.Thread(target=self.handleNewConnections).start()
            
    def sendALL(self,message):
        '''Sends a message to all other users from the current user'''
        print('sending',message)
        for user in self.connectionList:
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
        for user in self.connectionList:
            print('user',user)
            user.send(self.formatMessage(message,username).encode('utf-8'))
            
    def connectionHandler(self,user):
        '''Given a user, waits for them to input a message and then sends it to other users'''
        global running
        print('There are currently',threading.active_count(),'users active')
        while running:
            try:
                print('waiting on input from user: ',user)
                inputStr=user.conn.recv(4096).decode('UTF-8')
                if inputStr[0:8]==("setName"):
                    if(len(inputStr[8:])>0):
                        oldname=user.getName()
                        self.sendALL(oldname, "changed their username to ", inputStr[8:])
                    else:
                        user.conn.send(("You tried to set your name to an invalid name").encode('utf-8'))
                elif inputStr=="list":
                    user.conn.send(("Users connected: ",self.connectionList.values()).encode('utf-8'))
                elif inputStr=='quit':
                    user.conn.send(("Bye").encode('utf-8'))
                    user.conn.close()
                    self.sendALL(self.connectionList[user],"has disconnected")
                    self.connectionList.remove(user)
                    #kills thread                    
                    return None
#                elif inputStr=='':
#                    if user in self.connectionList.keys():
#                            self.sendALL(self.connectionList[user],"has disconnected")
#                            self.connectionList.remove(user)
                else:
                    self.sendAll(user,inputStr)
                    print('all good')
            except:
                if user in self.connectionList:
                    user.conn.close()
                    self.sendALL("User " + user.getName() + " disconnected.")
                    self.connectionList.remove(user)
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