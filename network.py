import networkx as nx

class NetworkSimulator:
    def __init__(self):
        self.graph = nx.Graph()

    def load_default_network(self):
        edges = [
            ('A', 'B', 4, 8),
            ('A', 'C', 2, 7),
            ('B', 'D', 5, 6),
            ('C', 'D', 1, 9),
            ('C', 'E', 7, 5),
            ('D', 'E', 3, 8),
            ('D', 'F', 6, 7),
            ('E', 'F', 2, 9)
        ]

        for node1, node2, weight, reliability in edges:
            self.graph.add_edge(node1, node2, weight=weight, reliability=reliability)

    def get_nodes(self):
        return list(self.graph.nodes)

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def generate_routes(self, source, destination):
        try:
            routes = list(nx.all_simple_paths(self.graph, source=source, target=destination))
            route_details = []

            for route in routes:
                total_cost = 0
                reliabilities = []

                for i in range(len(route) - 1):
                    edge_data = self.graph[route[i]][route[i + 1]]
                    total_cost += edge_data.get("weight", 1)
                    reliabilities.append(edge_data.get("reliability", 1))

                route_details.append({
                    "path": route,
                    "cost": total_cost,
                    "hops": len(route) - 1,
                    "reliability": min(reliabilities) if reliabilities else 0
                })

            return route_details

        except nx.NetworkXNoPath:
            return []
        except nx.NodeNotFound:
            return []

    def remove_node(self, node):
        if node in self.graph:
            self.graph.remove_node(node)

    def remove_edge(self, node1, node2):
        if self.graph.has_edge(node1, node2):
            self.graph.remove_edge(node1, node2)

    def reset_network(self):
        self.graph.clear()
        self.load_default_network()