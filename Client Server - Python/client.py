
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

# client.py
import socket 


def Main():
	port = 5000 # Reserve a port for your service.
	host = socket.gethostname() # Get local machine name

	s = socket.socket() # Create a socket object (TCP)
	s.connect((host,port)) #Tell the socket to connect at the host/port of the server

	print "Welcome to the Stankevix Server, choose a option:"
	print "Upload File --> [U]"
	print "Download File --> [D]"
	choice = raw_input("Option: -->")

	#Check if the file is already uploaded at the server
	if choice == 'D':
		filename = raw_input("filename: --->")
		s.send(filename) #send the file name to the server.
		data = s.recv(1024) #check if the file exists

		#If the files exists at the server
		if data[:6] == 'EXISTS':
			filesize = long(data[6:])
			message = raw_input("File Exists, "+ str(filesize)+\
							"Bytes, Do you want to download it?(Y/N) -->")
			#If the user choose YES, so send a message to the server
			if message == 'Y':
				s.send('OK')
				f = open('downloaded_'+filename, 'wb')

				#start receiving the data
				data = s.recv(1024)
				totalRecv = len(data)
				f.write(data)

				while totalRecv < filesize:
				 	data = s.recv(1024)
				 	totalRecv += len(data)
				 	f.write(data)
				 	print "{0:.2f}".format((totalRecv/float(filesize))*100)+\
				 			"% Done"
				 	print "Completed Download"

		else:
			s.send("ERROR")
			
	elif choice == 'U':
		
		message = 'Y'
		if message == 'Y':
			filename = raw_input("filename? --->")
			s.send(filename)
				 
			f = open('new_'+filename, 'w+')
			
			l = f.read(1024)
			print 'Sending...'
			s.send(l)

			while l != "":
				print 'Sending...'
				s.send(l)
				l = f.read(1024)
			
			f.close()
			print "Done Sending"
	
		else:
			s.send("ERROR")
	else:
		s.send("ERROR")
	s.close()

if __name__ == '__main__':
	Main()




