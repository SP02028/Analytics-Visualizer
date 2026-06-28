class Graph:
    def init (self, directed=False):
        self.directed = directed
        self.nodes = set()
        self.adj = {}
    def add_node(self, u):
        self.nodes.add(u)
        if u not in self.adj:
            self.adj[u] = []

    def add_edge(self, u, v, w=1):
        self.add_node(u)
        self.add_node(v)
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
