# this module will be imported in the into your flowgraph
import socket
# import string
import json  # To save variables as json
import ntpath  # To retrieve file name out of address
import os.path
from os import path

# Declaring class for "shared variable" object (communication between flowcharts)
class Shared_Variable:
	names = [] # List of variable names
	values = [] # List of variable values
	shared_variables = [] # List of variables set on init
	def __init__(self,shared_variables_):
		self.shared_variables = shared_variables_
		pass
	def clear(self):
		self.names = []
		self.values = []
	def save_variables(self, tt):
		# try:
			self.clear()
			for variable in self.shared_variables:
				self.names.append(variable)
				self.values.append(eval("tt.get_{}()".format(variable)))
			# Saving in json file
			f = open("shared_variables.json", "w")
			f.write(json.dumps(self.__dict__))
			f.close()
		# except:
		# 	pass
	def retrieve_variables(self, tt):
		# Check if file exist
		if(path.exists("shared_variables.json")):
			with open("shared_variables.json") as f:
				content = f.readline()
				self.__dict__ = json.loads(content)
			# Once read, remove it	
			os.remove("shared_variables.json")	
		
# 

def server(tt):
	while True:
		# Create list of shared variables
		shared_variables = ["entry_var_sample_rate_osmosdr","entry_var_measured_frequency"]
		sFile = Shared_Variable(shared_variables)
		#Save current local variables to share them
		sFile.save_variables(tt)

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
							# Changing local variables
							message = message.replace('>','').strip()
							[var_name, var_value] = message.split("=")
							command = "tt.{}=float({})".format(var_name, var_value)
							exec(command) 
							command = "tt.set_{}(float({}))".format(var_name, var_value)
							exec(command) 
							print("The new value of the variable {} is: {}".format(var_name, var_value))
							message = "" # Reset message variable

							# Save current values on "shared variables" file
							sFile.save_variables(tt)
						except:
							message = "" # Reset message variable
							print("Error: variable not set")						
					# Quit
					if 'quit' in data:
						print("Closing connection...")
						sock.shutdown(socket.SHUT_RDWR)
						sock.close()
						break # Back to listen loop
			# C