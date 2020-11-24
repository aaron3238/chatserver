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

Where the hostname is the IP address of the server the client will connect to, and the
port number is the port number that the server will be running on