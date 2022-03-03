import json  # To save variables as json

import os.path
from os import path

# # Declaring class for variable object (communication between flowcharts)
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
	# def save_variables(self):
	# 	# try:
	# 		for variable in shared_variables:
	# 			self.names.append(variable)
	# 			self.values.append(("tt.get_{}()".format(variable)))
	# 		# Saving in json file
	# 		f = open("shared_variables.json", "w")
	# 		f.write(json.dumps(self.__dict__))
	# 		f.close()
		# except:
			# pass
	def retrieve_variables(self):
		# Check if file exist
		if(path.exists("shared_variables.json")):
			with open("shared_variables.json") as f:
				content = f.readline()
				self.__dict__ = json.loads(content)
			pass
		pass
# # 

# # Create list of shared variables
shared_variables = ["sample_rate_osmosdr","measured_frequency"]
sFile = Shared_Variable(shared_variables)
# sFile.clear()
# #Save current local variables to share them
# sFile.save_variables(shared_variables)
# shared_variables.append("testing")
# sFile.clear()
# sFile.save_variables(shared_variables)

# # print(json.dumps(sFile, default=vars))
print(json.dumps(sFile.__dict__))
sFile.retrieve_variables()
print(json.dumps(sFile.__dict__))

os.remove("shared_variables.json")