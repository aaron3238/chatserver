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
from datetime import datetime
import time
import logging
import chatlib

global MAXBUFFERSIZE
MAXBUFFERSIZE = 2048

def log(message):
	f = open("chatlog.txt", "a")
	print(message)
	f.write(message)
	f.close()


def clientthread(conn, addr, clientNicknames, list_of_clients, end_event, threadStream):
	# nickname collection 
	
	while end_event.is_set():
		uniqueName = True
		nickname = ""		
		message = conn.recv(MAXBUFFERSIZE) 
		nickname = message.rstrip() # get rid of the newline
		if nickname == "BYE": # in case the client disconnects before making a nickname
			print(str(addr) + " Left before creating a nickname")
			remove(conn, list_of_clients)
			return
		if re.match("^[a-zA-Z0-9]{2,30}$", nickname): # ensure the nickname is alphanumeric, no spaces allowed

			for name in clientNicknames: # ensure the nickname is unique
				if name == nickname:
					uniqueName = False
			if uniqueName:
				conn.send("READY")
				clientNicknames.append(nickname)
				dateTime = datetime.now()
				threadStream[0] = str(dateTime) + " " + str(addr) + " " + nickname + "\n"
				print(threadStream[0])
				broadcast(nickname, conn, list_of_clients)
				break
			else:
				conn.send("RETRY")
		else:
			conn.send("INVALID")
			
	# start waiting for regular messages
	while end_event.is_set(): 
			try: 
				message = conn.recv(2048) 
				message = message.rstrip() # strip newlines

				if message == "BYE": # if client disconnects
					message_to_send = "<" + nickname + ">" " left the chatroom.\n"
					print(message_to_send)
					broadcast(message_to_send, conn, list_of_clients) # let everyone know 
					clientNicknames.remove(nickname) # remove from list of nicknames
					remove(conn, list_of_clients) # remove the connection
					break
				elif message: 
					threadStream[0] = nickname + ":" + message + "\n"
					# Calls broadcast function to send message to all 
					message_to_send = "<" + nickname + "> " + message 
					broadcast(message_to_send, conn, list_of_clients) 

				else: 
					# if the message is empty or broken remove the connection
					remove(conn, list_of_clients) 
			except: 
				continue
	return

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
	server = chatlib.socket_create(); 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	server.setblocking(0)


	# create an event to signal subthreads to end
	end_event = threading.Event()
	end_event.set()


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

	threadStream = [" "]
	
	
	while True: 
		#print "here"
		if threadStream[0] != " ":
			log(threadStream[0])
			threadStream[0] = " "
		try:
			# Get socket conn and address from client
			
			try:
				conn, addr = server.accept()
				list_of_clients.append(conn) 
				conn.send("HELLO")
				time.sleep(1)
				
				# Add conn to a list
				
				
				#start_new_thread(clientthread,(conn,addr, clientNicknames))	 
			
				try: 
					t = threading.Thread(target=clientthread, args=(conn, addr, clientNicknames, list_of_clients, end_event, threadStream))
					threads.append(t)
					#t.daemon = True # set the client threads to daemons so they end if the main thread ends
					t.start()
				except Exception as e:
					print("Error starting thread: ", e)
			except:
				pass
		
		except KeyboardInterrupt:
			message = "SERVER CLOSING IN 5 SECONDS"
			print("\n" + message)
			broadcast(message, server, list_of_clients)
			time.sleep(5)
			message = "SERVER CLOSED"
			broadcast(message, server, list_of_clients)
			end_event.clear() # trigger the event so that the subthreads end their while loops
			for t in threads:
				t.join()
			for conns in list_of_clients:
				conns.close()
			server.close() 
			return
		
	
	return


if __name__ == '__main__':
    main()