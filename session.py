import os
from time import time
from http import cookies
from hashlib import sha512

#create session folder
directory=os.environ["TMPDIR"]+'/pysession/'
if not os.path.exists(directory):
	os.makedirs(directory)

class Session():
	def __init__(self,sid):
		if not sid:	#if no sid given
			now=str(time())
			now=now.encode()
			hashsid=sha512()
			hashsid.update(now)
			self.sid=hashsid.hexdigest()

		else:
			self.sid=sid

		#create folder for users session
		self.sessdir=directory+"/"+self.sid
		if not os.path.exists(self.sessdir):
			os.makedirs(self.sessdir)

	def values(self):	#list all available keys
		return os.listdir(self.sessdir)

	def __str__(self):
		returnme={}

		for item in self.values():
			returnme[item]=self[item]

		return str(returnme)

	def __repr__(self):
		return "<Session object with sid "+self.sid+">"

	def __getitem__(self,key):
		try:
			file=open(self.sessdir+"/"+key,"r")
			returnme=file.readline()
			file.close()
		except FileNotFoundError:
			returnme=None

		return returnme

	def __setitem__(self,key,value):
		try:
			file=open(self.sessdir+"/"+key,"w+")
			file.write(value)
		except TypeError:
			file.write("")

		return


def session_start():
	COOKIE=cookies.SimpleCookie()
	COOKIE.load(os.environ.get('HTTP_COOKIE'))

	if not COOKIE.get("SESSION"):
		SESSION=Session(None)
		COOKIE["SESSION"]=SESSION
		print(COOKIE)

	else:
		SESSION=Session(COOKIE["SESSION"].value)

	return SESSION

def session_destroy():
	COOKIE=cookies.SimpleCookie()
	COOKIE.load(os.environ.get('HTTP_COOKIE'))
	COOKIE["SESSION"]["expires"]=-1
	print(COOKIE)

	for file in os.listdir(directory+COOKIE["SESSION"].value):
		os.remove(directory+COOKIE["SESSION"].value+"/"+file)
	os.removedirs(directory+COOKIE["SESSION"].value+"/")
