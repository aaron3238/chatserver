Contributors: Aaron Pritchard, David Nelson, Nick Morello, Nik Golombek
Filename: README.txt
Class: CSC328 
Prof: Dr. Frye 
Major: CS
Date: 23 November 2020
Assignment: Chat Server
Due: 24 November 2020
Execute: N/A
Description: Background info on chat server program

Building and Running the program:

The server code or client code must exist in the same directory as the dependency chatlib.py.

To run the server-side
program, this is the command and usage:

python server.py <hostname> <port number>

Here, <hostname> is the IP Address that the server will run and accept connections at,
and <port number> is an optional command line argument allowing the user to specify
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

chatlog.txt: Contains all the messages sent to the server as well as well the clients connected and disconnected.

No makefile was required because Python doesn’t require compilation

Responsibility Matrix:


                        Client.py      Server.py      Chatlib.py     README.txt
                        
Nicholas Morello                           X

Nik Golombek                               X

David Nelson                                              X              X

Aaron Pritchard             X

Our responsibility matrix ended up changing quite drastically during development. We ended up
just working as a group on most everything and just held discussions while coding. The client 
and library were so small compared to the server that it just ended up making no sense to 
rigorously hold to our originally defined responsibilities. 


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

A reasonable amount of clients will be connecting to the server at any given time.
User is running python 2.7. 

Assume the server is running before the client connects.

Discussion:

https://www.geeksforgeeks.org/simple-chat-room-using-python/
This resource was used during development.

Logging messages presented a slight issue in our main thread. The accept system call is a 
blocking system call so the main thread wasn’t able to check if something new was sent to 
the server that needed to be logged. This was fixed by setting the accept call to non-blocking 
which would then send an error when there was nothing to be read. This was resolved by catching 
that specific errno and passing it. 

Originally subthreads were set to daemon threads so that their execution ends when the main 
thread ends. This was working, but it seemed like a workaround and event handling/thread joining 
was set up to ensure proper closing of sockets and graceful shutdown when a Keyboard Interrupt 
was encountered. 