#!/usr/bin/python

from graph import diGraph;
import pycurl
import json
from io import BytesIO

#OAuth token: 5d268301033d2cca2ddaf31b3b505493f362fb7e



class repo:

	OAuth="5d268301033d2cca2ddaf31b3b505493f362fb7e"

	owner=""
	contributors=[] #stores tuple of [owner,% of stars they get]
	repo=""
	stargazers=[] #IDs of all the stargazers

	def __init__(self, owner,repo):
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

	def addContRepos(self,r,seenUser):
		for contr in self.contributors:
			if contr in seenUser:
				pass
			self.addUserRepo(r,contr[0])

	def addGazerRepos(self,r):
		for gazer in self.stargazers:
			self.addUserRepo(r,gazer)

	def addUserRepo(self, r, user,usersSeen):
		if user is not in usersSeen:
			response=self.callAPI('https://api.github.com/users/'+user+'/repos')
			usersSeen.append(user)
			#TODO: keep track of which users we've looked through
			for uRep in response:
				r.addRepo(user, uRep['name'])


		#uses pyculr to call API and returns response as a JSON dict
	def callAPI(self, request):
		print "calling: " + request

		buffer = BytesIO()
		c = pycurl.Curl()
		c.setopt(c.USERAGENT,"ebber:"+self.OAuth)
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
		print rl[0]+' ' +rl[1]
		r=repo(rl[0],rl[1])
		r.fillContributers(usersSeen)
		r.weightContributers()
		r.getStargazers()
		r.giveStars(G)
		r.addContRepos(que, usersSeen)
		#que.printRepos()
		print rl[0]+' over'
	except  Exception,e:
		break
G.draw()