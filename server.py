#!/usr/bin/python
# Contributors: Aaron Pritchard, David Nelson, Nick Morello, Nik Golombek
# Filename: server.py
# Class: CSC328 
# Prof: Dr. Frye 
# Major: CS
# Date: 22 November 2020
# Assignment: Chat Server
# Due: 24 November 2020
# Execute: python server.py
# Python Version: 2.7.5
# Purpose: Establishes a connection to a server with either TCP or UDP, which are
#          collected via command line arguments, and prints out a QOTD message from 
#          the specified server.
import socket 
import select 
import sys 
from thread import start_new_thread
import re

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048

def clientthread(conn, addr, clientNicknames): 

	# sends a message to the client whose user object is conn 
	conn.send("\nUsers currently connected: ")
	conn.send(str(clientNicknames))
	conn.send("\nEnter a unique nickname:")
	while True:
		uniqueName = True
		nickname = ""		
		message = conn.recv(MAXBUFFERSIZE) 
		nickname = message.rstrip()

		if re.match("^[a-zA-Z0-9]{2,30}$", nickname):

			for name in clientNicknames:
				if name == nickname:
					uniqueName = False
			if uniqueName:
				conn.send("READY")
				clientNicknames.append(nickname)
				print nickname + " connected"
				break
			else:
				print(clientNicknames)
				conn.send("RETRY")
		else:
			conn.send("Nickname must be alphanumberic and 2-30 Characters\n")
			conn.send("RETRY")
	
	while True: 
			try: 
				message = conn.recv(2048) 
				if message: 

					"""prints the message and address of the 
					user who just sent the message on the server 
					terminal"""
					print "<" + nickname + "> " + message 

					# Calls broadcast function to send message to all 
					message_to_send = "<" + nickname + "> " + message 
					broadcast(message_to_send, conn) 

				else: 
					"""message may have no content if the connection 
					is broken, in this case we remove the connection"""
					remove(conn) 
			except: 
				continue

# broadcast to all clients except the one sending it 
def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: # make sure it's not sending to itself
			try: 
				clients.send(message) 
			except: # can't send? 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients) 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection): 
	if connection in list_of_clients: # check if the connection is in the list of clients 
		list_of_clients.remove(connection) # remote it 

# Main Thread
def main():
	"""The first argument AF_INET is the address domain of the 
	socket. This is used when we have an Internet Domain with 
	any two hosts The second argument is the type of socket. 
	SOCK_STREAM means that data or characters are read in 
	a continuous flow."""
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

	# checks whether sufficient arguments have been provided 
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

	#Binds the server to an entered IP address and at the 
	#specified port number. 
	try:
		server.bind((IP_address, Port)) 
	except socket.error as err:
		print err
		exit()
	server.listen(100) 
	list_of_clients = [] 
	clientNicknames = []

	while True: 

		# Get socket conn and address from client
		conn, addr = server.accept()
		# Add conn to a list
		list_of_clients.append(conn) 

		conn.send("HELLO")
		
		start_new_thread(clientthread,(conn,addr, clientNicknames))	 

	conn.close() 
	server.close() 

if __name__ == '__main__':
    main()