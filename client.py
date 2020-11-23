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

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048
  
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
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

server.connect((IP_address, Port)) 
# sys.stdout.write("Enter a nickname: ")
# message = sys.stdin.readline() 
# server.send(message) 
# sys.stdout.write("<You>") 
# sys.stdout.write(message) 
# sys.stdout.flush() 
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
                message = socks.recv(MAXBUFFERSIZE) 
                if message == "SERVER CLOSED":
                    print message
                    server.close
                    exit()
                print message
            else: 
                message = sys.stdin.readline() 
                server.send(message) 
                sys.stdout.write("<You>") 
                sys.stdout.write(message) 
                sys.stdout.flush() 
    except KeyboardInterrupt:
        server.send("BYE")
        break

sys.stdout.flush() 
server.close() 
exit()