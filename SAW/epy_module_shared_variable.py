# this module will be imported in the into your flowgraph

import json  # To save variables as json
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
			self.clear()
			for variable in self.shared_variables:
				self.names.append(variable)
				self.values.append(eval("tt.get_{}()".format(variable)))
			# Saving in json file
			f = open("shared_variables.json", "w")
			f.write(json.dumps(self.__dict__))
			f.close()
	def retrieve_variables(self, tt):
		# Check if file exist
		if(path.exists("shared_variables.json")):
			self.clear()
			with open("shared_variables.json") as f:
				content = f.readline()
				self.__dict__ = json.loads(content)
			# Check if shared variables content is diff from local
			for i,variable in enumerate(self.names):
				var_name = variable
				var_value = self.values[i]
				if(eval("tt.get_{}()".format(var_name))!=self.values[i]):
					# value is different, setting variable
					command = "tt.set_{}(float({}))".format(var_name, var_value)
					exec(command) 
					print("The new value of the shared variable {} is: {}".format(var_name, var_value))
			# Once read, remove it	
			os.remove("shared_variables.json")	
		
# 

def main(tt):
	# Create list of shared variables
	shared_variables = ["entry_var_sample_rate_osmosdr","entry_var_measured_frequency"]
	sFile = Shared_Variable(shared_variables)
	while True:
		try:
			sFile.retrieve_variables(tt)
		except:
			pass