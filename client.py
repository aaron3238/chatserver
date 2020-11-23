#!/usr/bin/python
# Contributors: Aaron Pritchard, David Nelson, Nick Morello, Nik Golombek
# Filename: server.py
# Class: CSC328 
# Prof: Dr. Frye 
# Major: CS
# Date: 22 November 2020
# Assignment: Chat Server
# Due: 24 November 2020
# Execute: python client.py
# Python Version: 2.7.5
# Description: Client-side code for a python chatroom.
import socket 
import select 
import sys 
import time
import chatlib

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048
  
server = chatlib.socket_create(); 

if (len(sys.argv) != 2) and (len(sys.argv) != 3): 
	print "Correct usage: script, IP address, (optional) port number"
	exit()  
IP_address = str(sys.argv[1]) 
# takes second argument from command prompt as port number
if len(sys.argv) == 3:
	Port = int(sys.argv[2]) 
else:
  #default port
  Port = 8888

server.settimeout(5)
try:
    server.connect((IP_address, Port)) 
except Exception as e: 
    print(e)
    server.close()
    exit()
   

while True: 
    try:
    # maintains a list of possible input streams 
        sockets_list = [sys.stdin, server] 
  
    # """ There are two possible input situations. Either the 
    # user wants to give  manual input to send to other people, 
    # or the server is sending a message  to be printed on the 
    # screen. Select returns from sockets_list, the stream that 
    # is reader for input. So for example, if the server wants 
    # to send a message, then the if condition will hold true 
    # below.If the user wants to send a message, the else 
    # condition will evaluate as true"""
    
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

    
        for socks in read_sockets: 
            if socks == server:
                message = chatlib.read_msg(socks,MAXBUFFERSIZE) 
                if message == "SERVER CLOSED":
                    print message
                    server.close
                    exit()
                elif message == "HELLO":
                    print ("Enter a unique nickname:")
                    nickname = sys.stdin.readline()
                    chatlib.write_msg(server, nickname, MAXBUFFERSIZE)
                elif message == "READY":
                    print ("You may now talk in the chatroom. You may exit at anytime by using Ctrl + c.")
                elif message == "RETRY":
                    print("That nickname is already in use. Try again.")
                    nickname = sys.stdin.readline()
                    chatlib.write_msg(server, nickname, MAXBUFFERSIZE)
                elif message == "INVALID":
                    print("Nickname must be alphanumberic and 2-30 Characters. Try again.")
                    nickname = sys.stdin.readline()
                    chatlib.write_msg(server, nickname, MAXBUFFERSIZE)
                else:
                    print message
            else:
                message = sys.stdin.readline() 
                chatlib.write_msg(server, message, MAXBUFFERSIZE) 
                sys.stdout.write("<You>") 
                sys.stdout.write(message) 
                sys.stdout.flush() 
    except KeyboardInterrupt:
        chatlib.write_msg(server, "BYE", MAXBUFFERSIZE)
        break

sys.stdout.flush() 
server.close() 
exit()