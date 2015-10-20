#!/usr/bin/python
from githubScrapper import gitUser;

class student:

	#what we get from form
	gitHandle=""
	gradYear=2016
	university="" #TODO: Add this factor

	factor = {}  #github repos, github stars, github orgs
	factorWeight={'gitRepos':1,'gitStars':1, 'gitOrgs':1} 

	def __init__(self, gradYear, gitHandle, university):
		self.gitHandle = gitHandle
		self.gradYear = gradYear
		self.university = university

		self.fillGitFactors(self.gitHandle)


	def fillGitFactors(self, gitHandle): #github repos, github stars, github orgs
		git = gitUser(gitHandle)
		self.factor['gitRepos'] = len(git.getRepos()) 
		self.factor['gitStars'] = git.getStars()
		self.factor['gitOrgs'] = len(git.getOrgs())

	def printScore(self):
		score = 0
		for x in self.factor:
			score+= self.factor[x]*self.factorWeight[x]
		print score

	def updateFactorWeight(self, factor, newWeight=1):
		self.factorWeight[factor]=newWeight
		return self.factorWeight[factor]

	#that have been filled
	def getFactors(self):
		factorList= []
		for x in self.factor:
			factorList.append(x)
		return factorList

s = student(2019,'ebber')
s.printScore()
print s.getFactors()