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
# Description: Server-side code for a python chatroom.
import socket 
import select 
import sys 
import threading
import re
import time

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048

def clientthread(conn, addr, clientNicknames, list_of_clients): 

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
				joined = nickname + " connected"
				print(joined)
				broadcast(joined, conn, list_of_clients)
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
				

				if message == "BYE":
					message_to_send = "<" + nickname + ">" " left the chatroom.\n"
					print(message_to_send)
					broadcast(message_to_send, conn, list_of_clients)
					clientNicknames.remove(nickname)
					remove(conn, list_of_clients)
					return
				elif message: 
					print "<" + nickname + "> " + message 
					# Calls broadcast function to send message to all 
					message_to_send = "<" + nickname + "> " + message 
					broadcast(message_to_send, conn, list_of_clients) 

				else: 
					"""message may have no content if the connection 
					is broken, in this case we remove the connection"""
					remove(conn, list_of_clients) 
			except: 
				continue

# broadcast to all clients except the one sending it 
def broadcast(message, connection, list_of_clients): 
	for clients in list_of_clients: 
		if clients!=connection: # make sure it's not sending to itself
			try: 
				clients.send(message) 
			except: # can't send? 
				clients.close() 

				# if the link is broken, we remove the client 
				remove(clients, list_of_clients) 

"""The following function simply removes the object 
from the list that was created at the beginning of 
the program"""
def remove(connection, list_of_clients): 
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
	threads = []

	print("Server started successfully...")

	while True: 
		try:
			# Get socket conn and address from client
			conn, addr = server.accept()
			# Add conn to a list
			list_of_clients.append(conn) 

			conn.send("HELLO")
			
			#start_new_thread(clientthread,(conn,addr, clientNicknames))	 
			try: 
				t = threading.Thread(target=clientthread, args=(conn, addr, clientNicknames, list_of_clients))
				threads.append(t)
				t.daemon = True # set the client threads to daemons so they end if the main thread ends
				t.start()
			except Exception as e:
				print("Error starting thread: ", e)

		except KeyboardInterrupt:
			message = "SERVER CLOSING IN 3 SECONDS"
			broadcast(message, server, list_of_clients)
			time.sleep(3)
			for conns in list_of_clients:
				conns.close()

			server.close() 
			return


if __name__ == '__main__':
    main()