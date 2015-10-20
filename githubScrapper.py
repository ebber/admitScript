#!/usr/bin/python

import pycurl
import json;
from io import BytesIO

class gitUser:
	gHandle='';
	#lists
	repos=None; #list of the users repos, stored in a list - check github api for docs
	orgs = None
	#ints stored for easy access
	stargazers=0; ## of stars in all repos

	def __init__(self, gHandle=""):
		self.gHandle=gHandle;

	def getHandle(self):
		return self.gHandle

	#returns a list of all repos user owns, options are member, owner and all, 2nd param is force update
	def getRepos(self, typeOfRepo="all", force=False):
		if self.repos is  None or force:
			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://api.github.com/users/'+self.gHandle+'/repos?type='+typeOfRepo)
			c.setopt(c.WRITEDATA, buffer)
			c.perform()
			c.close()

			body = buffer.getvalue()
			# Body is a byte string.
			# We have to know the encoding in order to print it to a text file
			# such as standard output.
			self.repos = json.loads(body.decode('iso-8859-1'))
		return self.repos

	def getOrgs(self):
		if self.orgs is None:
			buffer = BytesIO()
			c = pycurl.Curl()
			c.setopt(c.URL, 'https://api.github.com/users/'+self.gHandle+'/orgs')
			c.setopt(c.WRITEDATA, buffer)
			c.perform()
			c.close()

			body = buffer.getvalue()
			# Body is a byte string.
			# We have to know the encoding in order to print it to a text file
			# such as standard output.
			self.orgs = json.loads(body.decode('iso-8859-1'))

		return self.orgs

	def getStars(self):
		stargazers=0
		for x in self.getRepos("owner"):
			self.stargazers+=x['stargazers_count']
		return self.stargazers
