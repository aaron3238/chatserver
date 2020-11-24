# Contributors: Aaron Pritchard, David Nelson, Nick Morello, Nik Golombek
# Filename: chatlib.py
# Class: CSC328 
# Prof: Dr. Frye 
# Major: CS
# Date: 22 November 2020
# Assignment: Chat Server
# Due: 24 November 2020
# Python Version: 2.7.5
# Description: Library functions for use with the server and client code.

import socket
import sys 

# Opens a new tcp socket as well as checking for errors
# Name: socket_create
# Arguments: None
# Return Value: None
def socket_create():

	try:
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return (newSocket)
	except socket.error as err:
		sys.stdout.write("Error creating socket: %s" % err)

# Reads a message from the socket
# Name: read_msg
# Arguments: sock - socket to read from
#            maxbuff - max buffer size of the message to read
# Return Value: None
def read_msg(sock, maxbuff):

	try:
		msg = sock.recv(maxbuff)
		return msg
	except socket.error as err:
		sys.stdout.write("Error reading data: %s" % err)

# write a message to a socket
# Name: write_msg
# Arguments: sock - socket to write to
#            msg - message to send
#            maxbuff - max buffer size of the message to send
# Return Value: 1 - if message was successfully sent
#              -1 - if there was an error
#               0 - if the message exceeds the specified buffer size
def write_msg(sock, msg, maxbuff):

	# encode example found at https://stackoverflow.com/questions/30686701/python-get-size-of-string-in-bytes
	length = len(msg.encode('utf-8'))
	if length <= maxbuff:
		try:
			sock.send(msg)
			return 1
		except socket.error as err: # can't send? 
			sys.stdout.write("Error writing data: %s" % err)
			sock.close() # closes socket if there was an error
			return -1
	else:
		print("Error: Message exceeds bufffersize")
		return 0
		