UNKNOWN = "not known"
class InputOutput:
	def __init__(self, inputData, name=""):
		self.name = name
		self.type = UNKNOWN
		if(isinstance(inputData, dict)) :
			if "id" in inputData :
				self.name = inputData["id"]
			if "type" in inputData :
				self.type = inputData["type"]
		elif(isinstance(inputData, str)) :
			#if name hasn't been assigned 
			if (self.name == "") :
				self.name = inputData

	def __str__(self):
		return "Input: {0} | Type: {1}".format(self.name, self.type)