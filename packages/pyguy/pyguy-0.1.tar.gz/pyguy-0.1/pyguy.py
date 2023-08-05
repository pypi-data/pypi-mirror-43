#Created by: developermind405@gmail.com

#Pyguy
import datetime
#################################################Exceptions#########################################################
class EditError(Exception):
	def __init__(self,reason):
		self.reason = reason
	def __str__(self):
		return self.reason
#####################################################################################################################
class guy:
	def __init__(self,name,older,gender,eye_color,size,language):
			self.name = name
			self.first_name = ""
			for i in self.name:
				if i != " ":
					self.first_name += i
				else:
					break 
			self.second_name = name.split(self.first_name+" ")[1]
				
			self.older = older
			self.gender = gender
			self.eye_color = eye_color
			self.size = size
			self.language = language
			self.sign = False
			self.values = {"name" : self.name,"first_name" : self.first_name,"second_name" : self.second_name, "older" : self.older, "gender" : self.gender, "eye_color" : self.eye_color, "size" : self.size,"language" : self.language}

	def get_values(self):	
		return self.values
	

	def get_birthday(self):
		now = int(datetime.datetime.now().year)
		older = self.older
		if not isinstance(older,int):
			try:
				older = int(older)
			except:
				raise TypeError("Older must be int")
		delta = now-older
		return delta

	def add_extra(self,theme,index):
		if not self.sign:
			self.values[theme] = index
		else:
			 raise EditError("Cannot change data, signed instance")
	
	def edit(self,theme,index):
		if not self.sign:
			if theme in self.values.keys():
				self.values[theme] = index
			else:
				raise IndexError("Theme not exist")
		else:
			raise EditError("Cannot change data, signed instance")
	def sign_guy(self):	
		if not self.sign:
			self.sign = True
		else:
			raise EditError("Cannot change data, signed instance")
####################################################################################################################################

class group:
	def __init__(self,group_name):
		self.name = group_name
		self.members = []
		self.value = {"Group_Name" : self.name,"members" : self.members}

	def add(self,newguy):
		ty = str(type(newguy))
		if ty == "<type 'instance'>":
			self.members.append(newguy)
		else:
			raise TypeError("Require instance")
	
	def remove(self,newguy):
		ty = str(type(newguy))
		if  ty == "<type 'instance'>":
			if newguy in self.members:
				self.members.remove(newguy)
			else:
				raise IndexError("Member not exist")
		else:
			raise TypeError("Require instance")

	def get_values(self):
		return self.value
		
	def add_theme(self,name):
		for member in self.members:
			command = "member.add_extra('"+name+"','-')"
			exec(command)
			






