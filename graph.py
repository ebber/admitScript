import networkx as nx

class diGraph:
	G = nx.DiGraph()
	nodes=[]

	def __init__(self,path="none"):
		if path!="none":
			self.G = nx.read_gpickle(path)

	def addID(self,node):
		self.G.add_node(node)
		self.nodes.append(node)

	def updateEdge(self,n1,n2,stars):
		try:
			cWeight=self.G.edge[n1][n2]["weight"]
		except KeyError:
			cWeight=0
		self.G.add_edge(n1,n2,weight=(stars+cWeight))
		return self.G.edge[n1][n2]["weight"]


	def draw(self):
		#print self.G.adjacency_list()
		for node in self.G.adjacency_iter():
			#print node
			for x in node:
				print str(x) +"\n"
		#for line in nx.generate_multiline_adjlist(self.G):
		#	print line

	def pickle(self, path):
		nx.write_gpickle(self.G,path)




