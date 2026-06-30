from flask import Flask, render_template, request, jsonify
from algorithms import bfs, dfs, dijkstra, all_paths, triadic_closure, smallest_robust_nodes, remove_nodes_disconnect, remove_edges_disconnect, smallest_robust_edges, get_node_degree, to_networkx
from graph import Graph
import networkx as nx

app = Flask(__name__)

def cytoscape_to_graph(elements):
    graph = Graph(directed=False)
    for element in elements:
        if 'source' in elem['data']:
            source = elem['data']['source']
            target = elem['data']['target']
            weight = elem['data'].get('weight', 1)
            graph.add_edge(source, target, weight)
        else:
            graph.add_node(elem['data']['id'])
    return graph
@app.route('/')
def index():
    return render_template('index.html')
@app .route('/api/bfs', methods=['POST'])
def api_bfs():
    try: 
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        start_node = list(graph.nodes)[0] if graph.nodes else None

        if not start_node:
            return jsonify({'error': 'Graph is empty'}), 400
        result = bfs(graph, start_node)
        return jsonify({'visited_nodes': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/dfs', methods=['POST'])
def api_dfs():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        start_node = list(graph.nodes)[0] if graph.nodes else None

        if not start_node:
            return jsonify({'error': 'Graph is empty'}), 400
        result = dfs(graph, start_node)
        return jsonify({'visited_nodes': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/dijkstra', methods=['POST'])
def api_dijkstra():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        start_node = list(graph.nodes)[0] if graph.nodes else None

        if not start_node:
            return jsonify({'error': 'Graph is empty'}), 400
        result = dijkstra(graph, start_node)
        return jsonify({'shortest_paths': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/all_paths', methods=['POST'])
def api_all_paths():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        nodes = list(graph.nodes)

        if len(nodes) < 2:
            return jsonify({'error': 'Graph must have at least two nodes'}), 400
        source,target = nodes[0], nodes[1]
        paths = all_paths(graph, source, target)

        visited = set()
        for path in paths:
            visited.update(path)
        return jsonify({'all_paths': paths, 'visited_nodes': list(visited)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/triadic_closure', methods=['POST'])
def api_triadic_closure():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        result = triadic_closure(graph)
        nx_graph = to_networkx(graph)

        triangles = set()
        for node in nx_graph.nodes():
            neighbors = list(nx_graph.neighbors(node))
            for i, n1 in enumerate(neighbors):
                for n2 in neighbors[i + 1:]:
                    if nx_graph.has_edge(n1, n2):
                        triangles.add(tuple(sorted([node, n1, n2])))
        return jsonify({
            'closure_coeff': result,
            'highlighted_nodes':list(triangles)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/smallest_robust_nodes', methods=['POST'])
def api_smallest_robust_nodes():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        result = smallest_robust_nodes(graph)
        return jsonify({'connectivity': result, 'message': f'Need to remove {result} nodes to disconnect'})
    except Exception as e:
        return jsonify({'error' : str(e)}), 400
@app.route('/api/smallest_robust_edges', methods=['POST'])
def api_smallest_robust_edges():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        result = smallest_robust_edges(graph)
        return jsonify({'connectivity': result, 'message': f'Need to remove {result} edges to disconnect'})
    except Exception as e:
        return jsonify({'error' : str(e)}), 400
@app.route('/api/remove_nodes_disconnect', methods=['POST'])
def api_remove_nodes_disconnect():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        nodes = list(graph.nodes)

        if len(nodes) < 2:
            return jsonify({'error': 'Graph must have at least two nodes'}), 400
        src, target = nodes[0], nodes[-1]
        connectivity, min_cut_nodes = remove_nodes_disconnect(graph, src, target)
        return jsonify({
            'connectivity': connectivity,
            'highlighted_nodes': list(min_cut_nodes),
            'source': src,
            'target': target,
            'message': f'Need to remove {connectivity} nodes to disconnect {src} and {target}'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/get_node_degree', methods=['POST'])
def api_get_node_degree():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        degrees = {}
        for node in graph.nodes:
            degrees[node] = get_node_degree(graph, node)
        max_degree_node = max(degrees, key=degrees.get) if degrees else None
       # min_degree_node = min(degrees, key=degrees.get) if degrees else None
        return jsonify({
            'degrees': degrees,
            'max_degree_node': [max_degree_node] if max_degree_node else None,
            #'min_degree_node': min_degree_node
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/diameter', methods=['POST'])
def api_diameter():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        nx_graph = to_networkx(graph)
        if nx.is_connected(nx_graph):
            diameter = nx.diameter(nx_graph.to_undirected())
            return jsonify({'diameter': diameter})
        else:
            return jsonify({'error': 'Graph is not connected'}), 400    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/radius', methods=['POST'])
def api_radius():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        nx_graph = to_networkx(graph)
        if nx.is_connected(nx_graph):
            radius = nx.radius(nx_graph.to_undirected())
            return jsonify({'radius': radius})
        else:
            return jsonify({'error': 'Graph is not connected'}), 400    
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/scc', methods=['POST'])
def api_scc():
    try:
        data = request.json()
        graph = cytoscape_to_graph(data['graph'])
        nx_graph = to_networkx(graph)
        sccs = list(nx.strongly_connected_components(nx_graph))
        largest_scc = max(sccs, key=len) if sccs else set()
        return jsonify({
            'num_components': len(sccs),
            'component_sizes': [len(scc) for scc in sccs],
            'highlighted_nodes': list(largest_scc)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400
@app.route('/api/eccentricity', methods=['POST'])
def api_eccentricity():
    pass

@app.route('/api/center', methods=['POST'])
def api_center():
    pass

@app.route('/api/periphery', methods=['POST'])
def api_periphery():
    pass

@app.route('/api/wcc', methods=['POST'])
def api_wcc():
    pass

@app.route('/api/degree_centrality', methods=['POST'])
def api_degree_centrality():
    pass

@app.route('/api/closeness_centrality', methods=['POST'])
def api_closeness_centrality():
    pass

@app.route('/api/betweenness_centrality', methods=['POST'])
def api_betweenness_centrality():
    pass

@app.route('/api/betweenness_centrality_approx', methods=['POST'])
def api_betweenness_centrality_approx():
    pass

@app.route('/api/betweenness_subset', methods=['POST'])
def api_betweenness_subset():
    pass

@app.route('/api/edge_betweenness_centrality', methods=['POST'])
def api_edge_betweenness_centrality():
    pass

@app.route('/api/edge_betweenness_centrality_approx', methods=['POST'])
def api_edge_betweenness_centrality_approx():
    pass

@app.route('/api/edge_betweenness_subset', methods=['POST'])
def api_edge_betweenness_subset():
    pass

@app.route('/api/pagerank', methods=['POST'])
def api_pagerank():
    pass

@app.route('/api/hits', methods=['POST'])
def api_hits():
    pass
if __name__ == '__main__':
    app.run(debug=True, port = 5000)