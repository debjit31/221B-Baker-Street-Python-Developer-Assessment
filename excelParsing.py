## xlrd library is used to parse excel files
# datetime is used to create a datetime object 
import xlrd
import sys
import datetime
class ParseDocument:
	## initializing the constructor with filelocation as parameter
	def __init__(self, filelocation):
		## data is the parent json / dictionary conaining all the data 
		self.data={}
		self.filelocation = filelocation
		## workbook is the reference to the excel file
		self.workbook = xlrd.open_workbook(self.filelocation)
		## sheet points to the opened sheet in the excel file
		self.sheet = self.workbook.sheet_by_index(0)

	## function for extracting the header
	def createHeader(self):
		req_keys = ["Quote Number", "Date", "Ship To", "Ship From", "Name"]
		## buff is a temporary buffer to fetch data before pushing in the json
		buff =[]
		for i in range(10):
				for j in range(self.sheet.ncols):
					if self.sheet.cell_type(i,j) == 3:	## returns the type of data in the cell, 3 corresponds to time 
						exceltime = self.sheet.cell_value(i,j)
						time_tuple = xlrd.xldate_as_tuple(exceltime, 0)
						buff.append(datetime.datetime(*time_tuple))## creating a python datetime object in the format yyyy-mm-dd
					else:
						buff.append(self.sheet.cell_value(i,j))
				buff[:] = [str(x) for x in buff]
		## searching for keyword labels and pushing (key, value) pairs in the json 
		for i in range(len(buff)):
			if buff[i] == "Quote Number":
				self.data["Quote Number"] = buff[i+1]
			elif buff[i] == "Date":
				date = buff[i+1].split()
				self.data["Date"] = date[0]
			elif buff[i] == "Ship To":
				self.data["Ship To"] = buff[i+1]
			elif buff[i].find("Name") != -1:
				sn = buff[i].split(":")
				self.data["Name"] = sn[1]
		## checking for error
		mykeys = self.data.keys()
		for i in mykeys:
			if i not in req_keys:
				print("Warning : Header Required field not found " + i)
		self.data["Items"] = [] ## initializing the items list in the json / dictionary

	## funtion for extracting the item details
	def items(self):
		labels = ["LineNumber", "PartNumber", "Description", "Item Type", "Price"]
		end=0
		for i in range(9, self.sheet.nrows):
			buff = []
			items = {}
			## fetching data row wise for each item
			for j in range(self.sheet.ncols):
				if str(self.sheet.cell_value(i,j)) != "":
					buff.append(str(self.sheet.cell_value(i,j)))
			## creating the zip object and parsing it to a list to form label, value pair
			pairs = list(zip(labels, buff))
			## deleting the unwanted label, value pairs
			for c in pairs:
				if c[0] == "Item Type":
					pairs.remove(c)
			for c in pairs:
				items[c[0]] = c[1]
			## end of file checking 
			if len(items) > 2:
				self.data["Items"].append(items)
		print(self.data)

if __name__ == "__main__":
	## getting filename from command line
	filename = sys.argv[1]
	## to store the file location of the excel sheet 
	file_location = "C:/Users/Debjit/OneDrive/Desktop/Debjit Chattopadhyay_BakerStreetAssessmentSolution/{}".format(filename)
	## initialize the class with the file location
	pd = ParseDocument(file_location)
	## method call to parse and read the header in the specified format
	pd.createHeader()
	## method call  to parse and read the item list in the specified format
	pd.items()


