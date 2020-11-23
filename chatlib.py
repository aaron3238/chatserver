import socket
import sys 

def socket_create():

	try:
		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return (newSocket)
	except socket.error as err:
		sys.stdout.write("Error creating socket: %s" % err)

def read_msg(sock, maxbuff):

	try:
		msg = sock.recv(maxbuff)
		return msg
	except socket.error as err:
		sys.stdout.write("Error reading data: %s" % err)
	
def write_msg(sock, msg, maxbuff):

	# encode example found at https://stackoverflow.com/questions/30686701/python-get-size-of-string-in-bytes
	length = len(msg.encode('utf-8'))
	if length <= maxbuff:
		try:
			sock.send(msg)
			return 1
		except: # can't send? 
			sock.close()
			#Need code to 
			return 0
	else:
		print("Error: Message exceeds bufffersize")
		return -1
		