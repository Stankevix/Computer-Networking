"""
/* =====================================================================
 * Universidade Federal de São Carlos - Campus Sorocaba
 * Redes - 2016/1
 * Orientação: Prof Fabio Verdi
 * 
 * Conexao Client e Server
 *
 * Trabalho 1
 *
 * Março de 2016
 * 
 * Gabriel Stankevix Soares		|	511340
===================================================================== */

"""

# server.py
import socket
import threading 
import os

#ThreadingFunction
def RetrFile(name, sock):
	#Receive data from the socket. 
    #The return value is a string representing the data received.
	filename = sock.recv(1024)
	if os.path.isfile(filename): #Check if there's a file
		sock.send("EXISTS " + str(os.path.getsize(filename))) #Send data to the socket.
		userResponse = sock.recv(1024) #receive a message from the client
		
		#Get the response to the user
		#grab the first 2 chars and check if they are equal
		if userResponse[:2] == 'OK': #if the client want to download the file, userResponse is going to be equal OK
			with open(filename, 'rb') as f:
				bytesToSend = f.read(1024)
				sock.send(bytesToSend)

				#case for files like images etc
				while bytesToSend != "":
					bytesToSend = f.read(1024)
					sock.send(bytesToSend)
	else:
		#sock.send("ERROR")
		#userResponse = sock.recv(1024) #userResponse receive oOK to upload

		print 'Receiving...'
		f = open('uploaded_'+filename, 'wb') #open a new file
		l = sock.recv(1024)
		while l != "":
			print "Receiving..."
			f.write(l)
			l = sock.recv(1024)
		f.close()
		print "Done Receiving!"
		sock.shutdown(socket.SHUT_WR)

	sock.close()

def Main():
	port = 5000 # Reserve a port for your service.
	s = socket.socket() # Create a socket object
	host = socket.gethostname() # Get local machine name
	s.bind((host,port)) # Bind to the port
	s.listen(5) # Now wait for client connection.

	print "Server Started..."
	#while this program is running
	while True:
		#The socket must be bound to an address and listening for connections
		conn, addr = s.accept()
		# conn is a new socket object usable to send and receive data on the connection
    	#address is the address bound to the socket on the other end of the connection.
		
		print "Client connected IP:<"+str(addr)+">"
		#create a thread
		t = threading.Thread(target = RetrFile, args =("retrThread", conn) )
		t.start()
	s.close()



if __name__ == '__main__':
	Main()