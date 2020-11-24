Building and Running the program:

server.py, client.py and chatlib.py must all be in the same directory. To run the server-side
program, this is the command and usage:

python server.py <hostname> <port number>

Here, the <hostname> is the IP Address that the server will run and accept connections at,
and the <port number> is an optional command line argument allowing the user to specify
which port number the server will run at and accept client connections from.

The user should run server.py before running client.py, ensuring that there is a server
up and running for the client to connect to.

To run the client-side portion of the network program, this is the command and usage:

python client.py <hostname> <port number>

Where <hostname> is the IP address of the server the client will connect to, and the
port number is the port number that the server will be running on. <port number> is
an optional command line argument allowing the client to specify the port number the
server is running on, if known.



File Manifest:

server.py: Contains the Python code for running the chat server, which is responsible for 
receiving new connections from clients, receiving messages from clients, and sending
messages received from clients out to all other clients

client.py: Contains the Python code for clients communicating with the chat server.
Multiple instances of client.py can be run at the same time, allowing multiple clients
to send messages to the chat server, which will forward their messages to each other,
allowing the clients to communicate

chatlib.py: Contains functions used by both client and server for opening new sockets,
reading from sockets, and writing to sockets, integrating the appropriate error-checking
required for each of those tasks in each function



Responsibility Matrix:


                        Client.py      Server.py      Chatlib.py     README.txt
                        
Nicholas Morello                           X

Nik Golombek                               X

David Nelson                                              X              X

Aaron Pritchard             X


Protocol:

The following messages sent back from the client to the server or vice-versa have the 
following meanings according to our chat server protocol:

HELLO – sent by server upon client connection
BYE – sent by client on disconnect
NICK – sent by client and contains the user’s selected nickname
READY – sent by server after successful registration (nickname)
RETRY – sent by server if nickname selected is not unique
INVALID - sent by server if nickname selected does not conform to nickname standards

Assumptions:

A reasonable amount of clients will be connecting to the server at any given time





