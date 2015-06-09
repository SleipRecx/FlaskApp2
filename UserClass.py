import time
class Users():


	def __init__(self,username,password,isAdmin):

		self.username = username
		self.password = password
		self.member_since = time.strftime("%d/%m/%Y")
		self.isAdmin = isAdmin


	def getUserName(self):
		return self.username



	def getMemberDate(self):
		return self.member_since

	def isAdmin(self):
		return isAdmin


