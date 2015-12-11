#!/usr/bin/python

from graph import diGraph;
import pycurl
import json
from io import BytesIO



class repo:

	OAuth=""

	owner=""
	contributors=[] #stores tuple of [owner,% of stars they get]
	repo=""
	stargazers=[] #IDs of all the stargazers

	def __init__(self, owner,repo):
		self.contributors=[]
		self.stargazers=[]
		self.owner=owner
		self.repo=repo


	def fillContributers(self):	
		response= self.callAPI('https://api.github.com/repos/'+self.owner+'/'+self.repo+'/contributors')
		for i in range(0, len(response)):
			self.contributors.append([response[i]['login'],1.0])
			#print self.contributors[i]


	#make this porportional to commits
	def weightContributers(self):
		numOfContributers=len(self.contributors)
		sumOfCont=0.0
		for i in range(0,numOfContributers+1):
			sumOfCont+=i
		#print sumOfCont
		for i in range(0,numOfContributers):
			self.contributors[i][1]=(numOfContributers-i)/sumOfCont
			#print self.contributors[i]

	def getStargazers(self):
		response = self.callAPI('https://api.github.com/repos/'+self.owner+'/'+self.repo+'/stargazers')
		for i in range(0, len(response)):
			self.stargazers.append(response[i]['login'])
			#print self.stargazers[i]

	def addNode(self, g, node):
		g.addID(node)


	def giveStars(self,g):
		for star in self.stargazers:
			self.addNode(g,star)
			for contr in self.contributors:
				self.addNode(g,contr[0])
				g.updateEdge(star,contr[0],contr[1])

	def addContRepos(self,r,usersSeen):
		for contr in self.contributors:
			if contr in usersSeen:
				pass
			self.addUserRepo(r,contr[0],usersSeen)

	def addGazerRepos(self,r,usersSeen):
		for gazer in self.stargazers:
			self.addUserRepo(r,gazer,usersSeen)

	def addUserRepo(self, r, user,usersSeen):
		if not user in usersSeen:
			response=self.callAPI('https://api.github.com/users/'+user+'/repos')
			usersSeen.append(user)
			#TODO: keep track of which users we've looked through
			for uRep in response:
				r.addRepo(user, uRep['name'])
		else:
			#print "we've seen you before"
			pass

	def returnStargazers(self):
		return self.stargazers

	def returnContributers(self):
		return self.contributors

		#uses pyculr to call API and returns response as a JSON dict
	def callAPI(self, request):
		print "calling: " + request

		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(pycurl.USERPWD,"ebber:"+self.OAuth)
		c.setopt(c.URL, request)
		c.setopt(c.WRITEDATA, buffer)
		c.perform()
		c.close()

		body = buffer.getvalue()
			# Body is a byte string.
			# We have to know the encoding in order to print it to a text file
			# such as standard output.
		return json.loads(body.decode('iso-8859-1'))


#repo que
class rQue:
	r=[]
	index=0
	def __init__(self):
		pass

	def addRepo(self,owner, repo):

		for rep in self.r:
			if [owner,repo] == rep:
				return;
		self.r.append([owner,repo])


	def getNext(self):
		self.index=self.index+1
		return self.r[self.index-1]

	def isEmpty(self):
		return self.index>=len(self.r)

	def printRepos(self):
		for i in range(self.index, len(self.r)):
			print self.r[i]



G=diGraph()
que = rQue()
usersSeen=[]

que.addRepo('ebber','NTDrone')
i=0

while not que.isEmpty() and i<5:
	try:

		i=i+1
		rl=que.getNext()
		#print rl[0]+' ' +rl[1]
		r=repo(rl[0],rl[1])
		r.fillContributers()
		#print "filled contributors"
		r.weightContributers()
		#print "weighted"
		r.getStargazers()
		#print "got gazers"
		r.giveStars(G)
		#print "stars given"
		r.addContRepos(que, usersSeen)
		#print "creps added"
		r.addGazerRepos(que, usersSeen)
		#que.printRepos()
		print rl[0] +':'+rl[1]+' stars: ' + str(len(r.returnStargazers())) +' among: ' + str(r.returnContributers())
	except ValueError, e:
		print e
		pass
	except  Exception,e:
		print e
		break
que.printRepos()
G.draw()