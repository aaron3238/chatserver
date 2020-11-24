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

# Set the nickname of the client
# Name: setNickname
# Arguments: none
# Return Value: none
def setNickname():
    nickname = sys.stdin.readline()
    chatlib.write_msg(server, nickname, MAXBUFFERSIZE)
    sys.stdout.flush()

server = chatlib.socket_create(); 

if (len(sys.argv) != 2) and (len(sys.argv) != 3): 
	print "Correct usage: script, IP address, (optional) port number"
	exit()  
IP_address = str(sys.argv[1]) 
# Takes second argument from command prompt as port number
if len(sys.argv) == 3:
	Port = int(sys.argv[2]) 
else:
  # Default port
  Port = 8888

server.settimeout(5)

# Tries to connect or gives the error otherwise
try:
    server.connect((IP_address, Port)) 
except socket.error as e: 
    print("Error Connectioning: %s" % e)
    server.close()
    exit()

# Var to keep track of the nickname status
nickSet = ""
while True: 
    try:
    # Maintains a list of possible input streams 
        sockets_list = [sys.stdin, server] 
  
        # Allows to differentiate between reading from the server or sending to the server
        read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

        for socks in read_sockets: 
            if socks == server:
                message = chatlib.read_msg(socks,MAXBUFFERSIZE) 
                #Decodes protocols sent from the server
                if message == "SERVER CLOSED":
                    print message
                    server.close
                    exit()
                elif message == "HELLO":
                    print("Enter a unique nickname:")
                    nickSet = "INIT"
                elif message == "READY":
                    print ("You may now talk in the chatroom. You may exit at anytime by using Ctrl + c.")
                    nickSet = True
                elif message == "RETRY":
                    print("That nickname is already in use. Try again.")
                    nickSet = "RETRY"
                elif message == "INVALID":
                    print("Nickname must be alphanumberic and 2-30 Characters. Try again.")
                    nickSet = "INVALID"
                else:
                    print message

            # Sends a nick name to the server
            elif nickSet == "INIT" or nickSet == "RETRY" or nickSet == "INVALID" :
                setNickname()
                nickSet = ""
            # If the client has a nickname then they can send messages
            elif nickSet == True:
                message = sys.stdin.readline()
                chatlib.write_msg(server, message, MAXBUFFERSIZE)
                sys.stdout.write("<You>")
                sys.stdout.write(message)
                sys.stdout.flush()
    
    except KeyboardInterrupt:
        # Tells the server that the client is disconnecting
        chatlib.write_msg(server, "BYE", MAXBUFFERSIZE)
        break

sys.stdout.flush()
server.close()
exit()