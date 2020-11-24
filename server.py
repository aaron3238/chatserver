#!/usr/bin/python
# Contributors: Aaron Pritchard, David Nelson, Nick Morello, Nik Golombek
# Filename: server.py
# Class: CSC328 
# Prof: Dr. Frye 
# Major: CS
# Date: 14 November 2020
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
from datetime import datetime
import time
import logging
import chatlib

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048

# log the date and time, client's IP address, client's nickname
# Name: log
# Arguments: Message - message to log to the file
# Return Value: None
def log(message):
	f = open("chatlog.txt", "a")
	print(message)
	f.write(message)
	f.close()

# Worker thread for each connected client
# Name: clientthread
# Arguments: conn,addr - connection to the client
#            clientNicknames - list of nicknames in use
#            list_of_clients - list of connected clients
#            end_event - tells the thread when it can end
#            threadStream - shared memory to send messages to the main thread
# Return: None
# Return Value: None
def clientthread(conn, addr, clientNicknames, list_of_clients, end_event, threadStream):
	# Nickname collection 
	
	while end_event.is_set():
		dateTime = datetime.now()
		uniqueName = True
		nickname = ""		
		message = chatlib.read_msg(conn,MAXBUFFERSIZE) 
		nickname = str(message.rstrip()) # Get rid of the newline
		if nickname == "BYE": # In case the client disconnects before making a nickname
			threadStream[0] = str(dateTime) + ", " + str(addr) + " Left before creating a nickname\n"
			remove(conn, list_of_clients)
			return
		if re.match("^[a-zA-Z0-9]{2,30}$", nickname): # Ensure the nickname is alphanumeric, no spaces allowed
			for name in clientNicknames: # Ensure the nickname is unique
				if name == nickname:
					uniqueName = False
			if uniqueName:
				chatlib.write_msg(conn, "READY", MAXBUFFERSIZE)
				clientNicknames.append(nickname)
				threadStream[0] = str(dateTime) + ", " + str(addr) + ", " + nickname + " connected.\n"
				message_to_send = "<" + nickname + ">" " joined the chatroom.\n"
				broadcast(message_to_send, conn, list_of_clients)
				break
			else:
				chatlib.write_msg(conn, "RETRY", MAXBUFFERSIZE)
		else:
			chatlib.write_msg(conn, "INVALID", MAXBUFFERSIZE)
			
	# Start waiting for regular messages
	while end_event.is_set(): 
			try: 
				message = chatlib.read_msg(conn,MAXBUFFERSIZE)
				message = message.rstrip() # Strip newlines

				if message == "BYE": # If client disconnects
					message_to_send = "<" + nickname + ">" " left the chatroom.\n"
					threadStream[0] = str(dateTime) + ", " + str(addr) + ", " + nickname + " disconnected.\n"
					broadcast(message_to_send, conn, list_of_clients) # Let everyone know 
					clientNicknames.remove(nickname) # Remove from list of nicknames
					remove(conn, list_of_clients) # Remove the connection
					break
				elif message: 
					threadStream[0] = nickname + ": " + message + "\n"
					# Calls broadcast function to send message to all 
					message_to_send = "<" + nickname + "> " + message 
					broadcast(message_to_send, conn, list_of_clients) 

				else: 
					# If the message is empty or broken remove the connection
					remove(conn, list_of_clients) 
			except: 
				continue
	return

# Broadcast to all clients except the one sending it
# Name: broadcast
# Arguments: message - message to broadcast
# 			 connection - connection that sent the message
# 			 list_of_client - clients to send the message to
# Return: None 
def broadcast(message, connection, list_of_clients): 
	for clients in list_of_clients: 
		if clients!=connection: # Make sure it's not sending to itself
			try: 
				chatlib.write_msg(clients, message, MAXBUFFERSIZE)
			except: # Can't send? 
				clients.close() 
				# If the link is broken, we remove the client 
				remove(clients, list_of_clients) 


# Removes unused connections from the list
# Name: remove
# Arguments: connection - the connection being checked
#			 list_of_clients - list of clients to check in
# Return: None
def remove(connection, list_of_clients): 
	if connection in list_of_clients: # Check if the connection is in the list of clients 
		list_of_clients.remove(connection) # Remote it 

# Main Thread
def main():
	
	# Creates a TCP socket
	server = chatlib.socket_create()
	try: 
		server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
		server.setblocking(0)
	except socket.error as err:
		print("Socket error: %s" % err)
		exit()

	# Create an event to signal subthreads to end
	end_event = threading.Event()
	end_event.set()


	# Checks whether sufficient arguments have been provided 
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

	# Binds the server to an entered IP address and at the 
	# Specified port number. 
	try:
		server.bind((IP_address, Port)) 
		server.listen(100)
	except socket.error as err:
		print ("Socket error: %s" % err)
		exit()
	 
	list_of_clients = [] 
	clientNicknames = []
	threads = []

	print("Server started successfully...")

	threadStream = [" "]
	
	while True: 
		if threadStream[0] != " ":
			log(threadStream[0])
			threadStream[0] = " "
		try:
			# Get socket conn and address from client
			
			try:
				conn, addr = server.accept()
				#add conn to list of connections
				list_of_clients.append(conn)
				chatlib.write_msg(conn, "HELLO", MAXBUFFERSIZE) 
			
				try: 
					t = threading.Thread(target=clientthread, args=(conn, addr, clientNicknames, list_of_clients, end_event, threadStream))
					threads.append(t)
					t.start()
				except Exception as e:
					print("Error starting thread: ", e)
			except socket.error as err: 
			# Catches errno11 because accept is no longer a blocking call
				if err.errno == 11:
					pass
				else:
					print("Socket error: %s" % err)
		
		except KeyboardInterrupt: # Close server
			message = "SERVER CLOSING IN 5 SECONDS"
			print("\n" + message)
			broadcast(message, server, list_of_clients)
			time.sleep(5) # Give time for clients to see server closing warning
			message = "SERVER CLOSED"
			broadcast(message, server, list_of_clients)
			end_event.clear() # Trigger the event so that the subthreads end their while loops
			for t in threads:
				t.join()
			for conns in list_of_clients:
				conns.close()
			server.close() 
			return


if __name__ == '__main__':
    main()