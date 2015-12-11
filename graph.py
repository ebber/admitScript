import networkx as nx

class diGraph:
	G = nx.DiGraph()

	def __init__(self):
		pass

	def addID(self,node):
		self.G.add_node(node)

	def updateEdge(self,n1,n2,stars):
		try:
			cWeight=self.G.edge[n1][n2]["weight"]
		except KeyError:
			cWeight=0
		self.G.add_edge(n1,n2,weight=(stars+cWeight))
		return self.G.edge[n1][n2]["weight"]

	def draw(self):
		for line in nx.generate_multiline_adjlist(self.G):
			print line



