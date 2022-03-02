# this module will be imported in the into your flowgraph
import socket
# import string

def server(tt):
	while True:
		# Configure socket
		sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('192.168.137.8',4242))
		# Listen
		print("Waiting for connection...")
		sock.listen(1)
		# Connected
		conn,addr=sock.accept()
		with conn:
			print('Connected from: ', addr)
			message = "" # Variable to store complete message
			while True:
				# Get text
				data=conn.recv(1)
				if data:
					data=data.decode()
					message = message+data
					# print(message)
					if '>' in message: # Delimeter to indicate end of message
						try:
							# Changing variables
							message = message.replace('>','').strip()
							[var_name, var_value] = message.split("=")
							command = "tt.set_{}(float({}))".format(var_name, var_value)
							exec(command) 
							print("The new value of the variable {} is: {}".format(var_name, var_value))
							message = "" # Reset variable
						except:
							message = "" # Reset variable
							print("Error: variable not set")						
					# Quit
					if 'quit' in data:
						print("Closing connection...")
						sock.shutdown(socket.SHUT_RDWR)
						sock.close()
						break # Back to listen loop