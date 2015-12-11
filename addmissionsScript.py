#!/usr/bin/python
from githubScrapper import gitUser;

class student:

	#what we get from form
	gitHandle=""
	gradYear=2016
	university="" #TODO: Add this factor
	git=None;
	#vars we gotta make

	factor = {}  #name:[func, value, weighting]

	def __init__(self, gradYear, gitHandle, university):
		self.gitHandle = gitHandle
		self.gradYear = gradYear
		self.university = university

		self.fillGit(gitHandle)

		self.factor['gitRepos']=[self.getGitRepos,0]
		self.factor['gitStars']=[self.getGStars,0]

		self.updateFactors()



		self.fillGit(self.gitHandle)

	def addFactor(name, quantifier, weighting, value=0):
		self.factor[name]=[quantifier,value,weighting]



	def fillGit(self, gitHandle): #github repos, github stars, github orgs
		self.git = gitUser(gitHandle)

	def getGitRepos(self):
 
	def getGStars(self):
		return self.git.getStars()

	def getGOrgs(self):
		return len(self.git.getOrgs())


	def updateFactors(self):
		for x in self.factor:
			self.factor[x][1] = self.factor[x][0]()


	def printScore(self, weights):
		print self.returnScore(weights)

	#weights is a dict of name:weight
	def returnScore(self, weights):
		score=0
		for x in weights:
			score+=self.factor[x[0]][1]*x[1]
		return score

	#that have been filled
	def getFactors(self):
		factorList= []
		for x in self.factor:
			factorList.append(x)
		return factorList

s = student(2019,'ebber','UIUC')
l=[]
for fact in s.getFactors():
	l.append([fact,1])
s.printScore(l)
#print s.getFactors()