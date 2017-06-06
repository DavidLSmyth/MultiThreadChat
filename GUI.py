# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:11:23 2016

@author: Marion
"""
from tkinter import *
from socket import *
from threading import *
import sys
import time


### main function###
def main():
    ###run UI###
    ###main can be used for debugging###
    print("in main")
    #root=Tk()  
    #root.resizable(width=FALSE,height=FALSE)
    Setup()    
    #root.mainloop()
 
        


class ClientUI:
    def __init__(self,username):
        self.root=Tk()
        self.root.resizable(width=FALSE,height=FALSE)
        self.root.protocol("WM_DELETE_WINDOW",self.close)        
        ####socket stuff
        ##self.ui=ClientUI(root)
        
        ###socket stuff
        
        self.running=True
        self.quitWhenReceive=False
        print("running")
        ##create client##
        #self.client=Client()
        ##topframe##
        topFrame=Frame(self.root)
        topFrame.grid(row=0)
        ##bottomframe##
        bottomFrame=Frame(self.root)
        bottomFrame.grid(row=1)
        ##sendbutton##
        sendButton=Button(bottomFrame,text="send",command=self.sendClick)
        sendButton.grid(row=1,column=0) 
        self.currentMessage=StringVar(self.root)
        ##text displayed##        
        self.mainText=Text(topFrame,height=20,width=80)
        self.mainText.grid()
        self.mainText.setvar(name='currentMessage')
        self.currentMessage.set("Hi")
        self.mainText.config(state=DISABLED)
        self.messagebox=Text(bottomFrame,width=50,height=5)
        self.messagebox.grid(row=0)
        self.messagebox.bind("<Return>",self.sendEnter)
        #text.setvar(currentMessage)
        ##scrollbar##
        scrollbar=Scrollbar(self.root)
        scrollbar.grid(row=0,column=2,ipady=140)
        ##perhaps this could be done elsewhere##
        self.mainText.config(yscrollcommand=scrollbar.set)
        
        self.host='localhost'
        self.port=8080
        self.s=socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.host,self.port))
        self.username=username
        self.s.send((self.username).encode('UTF-8'))
        #wait for input
        self.thread=Thread(target=self.receive)
        self.thread.start()        
        print('connected')        
        self.root.mainloop()
        
    def sendEnter(self,event):
        self.sendClick()
    
    def sendClick(self):
        print("displaying message")        
        message=self.messagebox.get("1.0",END)
        if message.replace('\n','')=='quit':
            self.quitWhenReceive=True
        self.messagebox.delete("1.0",END)
        self.sendmessage(message.replace("\n",""))
        #self.displayIncomingMessage(message)
        print(message.replace("\n",""))
        return message
    
    def displayIncomingMessage(self,message):
        print("displaying incoming message")
        self.mainText.config(state=NORMAL)
        self.mainText.insert(END,'\n'+message)
        self.mainText.config(state=DISABLED)
        
        #format the message in client or here?
    #####socket methods#####
    def sendmessage(self,message):
        self.s.send(message.encode('utf-8'))
        
    def receive(self):
        print("in receive")
        while True:
            data=self.s.recv(1024).decode('UTF-8')
            if len(data)>0:
                break
        #if data contains quit or something similar:
        #else:
        self.displayIncomingMessage(str(data))
        if self.quitWhenReceive:
            time.sleep(2)
            self.close()
        else:
            self.thread=Thread(target=self.receive)
            self.thread.start()
        
    def close(self):
        self.s.send("EXIT".encode('utf-8'))
        self.s.close()
        self.root.destroy()
        
class Setup:
    def __init__(self):
        self.root=Tk()
        self.root.resizable(width=FALSE,height=FALSE)
        self.root.protocol("WM_DELETE_WINDOW",self.close)
        self.enterChat=Button(self.root, text="Enter chat", command=self.begin)
        self.label=Label(self.root, text="Enter your username:")
        self.userNameBox=Text(self.root,height=1,width=20)       
        self.userNameBox.grid(row=0,column=2)            
        self.label.grid(row=0,column=0)
        self.enterChat.grid(row=1,rowspan=2)
        self.userNameBox.bind("<Return>",self.sendEnter)        
        self.root.mainloop()
    
    def sendEnter(self,event):
        self.begin()
        
    def begin(self):
        name=self.userNameBox.get("1.0",END)
        self.root.destroy()
        ClientUI(name)
        
    def close(self):
        self.root.destroy()
'''
class Client():
    def __init__(self):
        ##self.ui=ClientUI(root)
        self.host='localhost'
        self.port=8080
        self.thread=start_new_thread(receive)
        try:
            self.s=socket(AF_INET,SOCK_STREAM)
        except socket.error:
            print('failure')
            ##handle this properly
            sys.exit()
        self.s.connect(self.host,self.port)
        print('connected')
        
    def send(self,message):
        message=message+('\t'+time.localtime)
        self.s.send(message.encode('utf-8'))
    
    def receive(self):
        while True:
            data=self.s.recv(1024)
            if data:
                break
'''        
        
    
main()