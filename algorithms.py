from collections import deque
import networkx as nx
import heapq
import math
def bfs(graph, start):
    q=deque([start])
    visited = set([start])
    order = []

    while q:
        u = q.popleft
        order.append(u)

        for v, i in graph.adj.get(u,[]):
            if v not in visited:
                visited.add(v)
                q.append(v)
    return order

def dfs(graph, start):
    visited = set()
    order = []

    def go(u):
        visited.add(u)
        order.append(u)

        for v, i in graph.adj.get(u, []):
            if v not in visited:
                go(v)
    go(start)
    return order
def dijkstra (graph, start):
    #path: Sequence of nodes connected by edges, from start to end
    dist = {node: math.inf for node in graph.nodes}
    prev = {node: None for node in graph.nodes}

    dist[start] = 0
    pq = [(0,start)]
    while pq:
        d,u = heapq.heappop(pq)

        if d != dist[u]:
            continue
        for v, w in graph.adj.get(u, []):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev
def get_node_degree(graph, node, directed=False, degree_type="both"):
    if node not in graph:
        return 0
    if not directed:
        return len(graph[node])
    out_degree = len(graph[node])
    in_degree = sum(1 for source in graph if node in graph[source])

    if degree_type == "in":
        return in_degree
    elif degree_type == "out":
        return out_degree
    else: 
        return in_degree + out_degree
def to_networkx(graph):
    nx_graph = nx.DiGraph() if graph.directed else nx.Graph()
    for node in graph.nodes:
        nx_graph.add_node(node)
    for source, nbr in graph.adj.items():
        for target, weight in nbr:
                nx_graph.add_edge(source, target, weight=weight)
    if not graph.directed:
        nx_graph = nx.Graph().to_undirected()(nx_graph)
    return nx_graph
#network robustness: The abliity of a network to maintain its general structural properties when it faces failures or attacks (removal of nodes or edges)
#is general function of network maintained if something happens?
#ex airport closures, internet routing failures
def smallest_robust_nodes(graph):
    #returns the smallest number of nodes that can be removed from this graph in order to disconnect it
    return nx.node_connectivity(to_networkx(graph))
def remove_nodes_disconnect(graph, src, target):
    #how many nodes must be removed to discconect src and target, and shows which nodes those are
    return nx.node_connectivity(to_networkx(graph),src,target), nx.minimum_node_cut(to_networkx(graph),src,target)
def remove_edges_disconnect(graph, src, target):
    #how many edges must be removed to disconnect src and target, and shows which edges those are
    return nx.edge_connectivity(to_networkx(graph),src,target), nx.minimum_edge_cut(to_networkx(graph),src,target)
def smallest_robust_edges(graph):
    #returns the smallest number of edges that can be removed from this graph in order to disconnect it
    return nx.edge_connectivity(to_networkx(graph))
def all_paths(graph, source, target):
    #returns all simple paths from node a to node b by passing it along to other nodes in the network
    return sorted(nx.all_simple_paths(to_networkx(graph), source, target))

def triadic_closure(graph):
#the tendency for people who share connections in a social network to become connected
    nx_graph = to_networkx(graph)

    if nx_graph.number_of_nodes() == 0:
        return{
            "local clustering": {},
            "average_clustering": 0,
            "transitivity": 0.0,
            "triangles": 0.0
        }
    return {
    #Local clustering coefficient: Fraction of pairs of the node's friends that are friends with each other
     # pairs of C's connected nodes who are connected/degree(c) C 
        "local clustering": nx.clustering(nx_graph),
    #coefficient on whole network
        #- average local clustering coefficient over all nodes in graph
        "average_clustering": nx.average_clustering(nx_graph),
    #transitivity = 3*number of closed triads/number of open triads
 #- triangles are 3 nodes connected by 3 edges, triads are 3 nodes connected by 2 edges
    #Transitivity weights nodes with a higher degree higher
        "transitivity": nx.transitivity(nx_graph),
        "triangles": nx.triangles(nx_graph)
    }   
def diameter(graph):
    # Diameter of the graph (longest shortest path)
    diameter = nx.diameter(to_networkx(graph))
    return diameter
def radius(graph):
    # Radius of the graph (shortest longest path)
    radius = nx.radius(to_networkx(graph))
    return radius
def eccentricity(graph):
    # Eccentricity of the graph (maximum distance from a node to all other nodes)
    eccentricity = nx.eccentricity(to_networkx(graph))
    return eccentricity
def center(graph):
    # Center of the graph (node with minimum eccentricity)
    center = nx.center(to_networkx(graph))
    return center
def periphery(graph):
    # Periphery of the graph (nodes with maximum eccentricity)
    periphery = nx.periphery(to_networkx(graph))
    return periphery
#An undirected graph is connected if there is a path between every pair of nodes.
#connected components: subset of nodes such as every node in the subset is reachable from every other node in the subset, no other node has a path to any node in the subset
#these two methods return if a graph is strongly/weakly connected, and if so the connected components
def SCC(graph):
    # Strongly Connected Components
    #a directed graph is strongly connected if there is a directed path from every node to every other node
    if to_networkx(graph).is_strongly_connected():
        return True, list(nx.strongly_connected_components(to_networkx(graph)))
    else:
        return False, None
def WCC(graph):
    # Weakly Connected Components
    #a directed graph is weakly connected if there is an undirected path from every node to every other node
    if to_networkx(graph).is_weakly_connected():
        return True, list(nx.weakly_connected_components(to_networkx(graph)))
    else:
        return False, None
    pass
#centrality measures identify the most important nodes in a network
#ex.) influential nodes in a social network, nodes that disseminate info to many nodes, hubs in a transportation network, important web pages, nodes that prevent the network from breaking up
def degree_centrality(graph, directed, degree_type, desired_result):
    #assummption: important nodes have many connections
    #the most basic measure of centrality
    #directed: in-degree and out-degree
    #undirected: degree
    if not directed:
        degCent = nx.degree_centrality(to_networkx(graph))
    else:
        if degree_type == "in":
            degCent = nx.in_degree_centrality(to_networkx(graph))
        elif degree_type == "out":
            degCent = nx.out_degree_centrality(to_networkx(graph))
    if desired_result == "max":
        return max(degCent, key=degCent.get), degCent[max(degCent, key=degCent.get)]
    elif desired_result == "min":
        return min(degCent, key=degCent.get), degCent[min(degCent, key=degCent.get)]
    return degCent
def closeness_centrality(graph, desired_result, normal):
    # Closeness Centrality
    #NDOES THAT ARE IMPORTANT ARE CLOSE TO OTHER NODES
    closeCent = nx.closeness_centrality(to_networkx(graph), normalized = normal) #if the node is disconnected, do we adjust for the fraction of nodes reachable or only use the number of reachable nodes (T/F)
    if desired_result =="max":
        return max(closeCent, key=closeCent.get), closeCent[max(closeCent, key=closeCent.get)]
    elif desired_result == "min":
        return min(closeCent, key=closeCent.get), closeCent[min(closeCent, key=closeCent.get)]
    return closeCent
def betweenness_centrality(graph, desired_result, normal):
    #Betweenness Centrality
    #nodes that are important are those that lie on many shortest paths between other nodes
def pagerank():
    # PageRank
    pass
def hubs_and_authorities():
    # Hubs and Authorities
    pass
