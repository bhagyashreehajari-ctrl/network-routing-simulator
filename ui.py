import tkinter as tk
from tkinter import ttk, scrolledtext
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from algorithm import safest_path_maxmin, merge_sort, binary_search
from network import NetworkSimulator


class EmergencyNetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Routing Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.network = NetworkSimulator()
        self.network.load_default_network()
        self.graph = self.network.graph
        self.routes = []

        self.setup_styles()
        self.create_ui()
        self.draw_graph()
        self.update_status("Ready")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def create_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="🚨 Emergency Network Routing Simulator",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack(pady=15)

        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_panel = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))

        self.create_input_section(left_panel)
        self.create_button_section(left_panel)

        right_panel = tk.Frame(content_frame, bg="#f0f0f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_output_section(right_panel)
        self.create_graph_section(right_panel)

        self.create_status_bar()

    def create_input_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="📝 Network Parameters",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame, text="Source:", bg="#ecf0f1").grid(row=0, column=0, sticky="w", pady=5)
        self.source_entry = tk.Entry(frame)
        self.source_entry.grid(row=0, column=1, pady=5)
        self.source_entry.insert(0, "A")

        tk.Label(frame, text="Destination:", bg="#ecf0f1").grid(row=1, column=0, sticky="w", pady=5)
        self.dest_entry = tk.Entry(frame)
        self.dest_entry.grid(row=1, column=1, pady=5)
        self.dest_entry.insert(0, "F")

        tk.Label(frame, text="Search Route:", bg="#ecf0f1").grid(row=2, column=0, sticky="w", pady=5)
        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Fail Node:", bg="#ecf0f1").grid(row=3, column=0, sticky="w", pady=5)
        self.fail_node_entry = tk.Entry(frame)
        self.fail_node_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Fail Edge (A-B):", bg="#ecf0f1").grid(row=4, column=0, sticky="w", pady=5)
        self.fail_edge_entry = tk.Entry(frame)
        self.fail_edge_entry.grid(row=4, column=1, pady=5)

    def create_button_section(self, parent):
        frame = tk.LabelFrame(
            parent,
            text="⚡ Operations",
            font=("Arial", 11, "bold"),
            bg="#ecf0f1",
            padx=10,
            pady=10
        )
        frame.pack(fill=tk.BOTH, padx=10, pady=10)

        buttons = [
            ("Generate Routes", self.generate_routes),
            ("Find Best Route", self.find_best_route),
            ("Sort Routes", self.sort_routes),
            ("Find Safest Route", self.find_safest_route),
            ("Search Route", self.search_route),
            ("Simulate Node Failure", self.simulate_node_failure),
            ("Simulate Edge Failure", self.simulate_edge_failure),
            ("Reset Network", self.reset_network)
        ]

        for text, cmd in buttons:
            tk.Button(frame, text=text, command=cmd).pack(fill=tk.X, pady=5)

    def create_output_section(self, parent):
        frame = tk.LabelFrame(parent, text="Output")
        frame.pack(fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(frame, font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True)

    def create_graph_section(self, parent):
        frame = tk.LabelFrame(parent, text="Graph")
        frame.pack(fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(5, 3))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_status_bar(self):
        self.status = tk.Label(self.root, text="Ready", bg="#34495e", fg="white")
        self.status.pack(fill=tk.X)

    def update_status(self, msg):
        self.status.config(text=msg)

    def display(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def clear_output(self):
        self.output.delete(1.0, tk.END)

    def draw_graph(self, highlight=None):
        self.ax.clear()
        pos = nx.spring_layout(self.graph, seed=42)

        nx.draw(
            self.graph,
            pos,
            ax=self.ax,
            with_labels=True,
            node_color="lightblue",
            node_size=1200,
            font_weight="bold"
        )

        edge_labels = {}
        for u, v, data in self.graph.edges(data=True):
            weight = data.get("weight", 0)
            reliability = data.get("reliability", 0)
            edge_labels[(u, v)] = f"{weight},{reliability}"

        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels, ax=self.ax)

        if highlight:
            edges = list(zip(highlight[:-1], highlight[1:]))
            nx.draw_networkx_edges(
                self.graph,
                pos,
                edgelist=edges,
                edge_color="red",
                width=3,
                ax=self.ax
            )

        self.canvas.draw()

    def generate_routes(self):
        self.clear_output()

        source = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()

        route_details = self.network.generate_routes(source, dest)

        if not route_details:
            self.display("Invalid nodes or no routes found")
            return

        self.routes = []

        self.display("Generated Routes:\n")
        self.display("Route | Cost | Hops | Reliability\n")

        for route in route_details:
            route_str = " → ".join(route["path"])
            self.routes.append((route_str, route["cost"]))

        for route_str, cost in self.routes:
            self.display(
                f"{route_str} | {cost} | {route['hops']} | {route['reliability']}"
            )

    def find_best_route(self):
        self.clear_output()

        source = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()

        try:
            path = nx.shortest_path(self.graph, source, dest, weight="weight")
            cost = nx.shortest_path_length(self.graph, source, dest, weight="weight")
            self.display("Best Route: " + " → ".join(path))
            self.previous_best = (path, cost)
            self.display(f"Total Cost: {cost}")
            self.draw_graph(path)
        except Exception:
            self.display("⚠️ No route available in the network")

    def sort_routes(self):
        self.clear_output()

        if not self.routes:
            self.display("Generate routes first")
            return

        self.routes = merge_sort(self.routes)

        self.display("Sorted Routes:\n")
        for route_name, cost in self.routes:
            self.display(f"{route_name} | {cost}")

    def find_safest_route(self):
        self.clear_output()

        source = self.source_entry.get().strip().upper()
        dest = self.dest_entry.get().strip().upper()

        path, cap = safest_path_maxmin(self.graph, source, dest)

        if path:
            self.display("Safest Route: " + " → ".join(path))
            self.display(f"Minimum Reliability: {cap}")
            self.draw_graph(path)
        else:
            self.display("No safe route found")

    def search_route(self):
        self.clear_output()

        if not self.routes:
            self.display("Generate routes first")
            return

        self.routes = sorted(self.routes, key=lambda x: x[0])
        target = self.search_entry.get().strip()

        result = binary_search(self.routes, target)

        if result:
            self.display(f"Found Route: {result[0]} | Cost: {result[1]}")
        else:
            self.display("Route not found")

    def simulate_node_failure(self):
        self.clear_output()

        node = self.fail_node_entry.get().strip().upper()

        if not node:
            self.display("Enter a node to remove")
            return

        self.network.remove_node(node)
        self.graph = self.network.graph
        self.routes = []
        self.display(f"Node {node} removed successfully")
        self.draw_graph()

    def simulate_edge_failure(self):
        self.clear_output()

        edge = self.fail_edge_entry.get().strip().upper()

        if "-" not in edge:
            self.display("Enter edge in format A-B")
            return

        n1, n2 = edge.split("-")
        self.network.remove_edge(n1, n2)
        self.graph = self.network.graph
        self.routes = []
        self.display(f"Edge {n1}-{n2} removed successfully")
        try:
            new_path = nx.shortest_path(self.graph, self.source_entry.get(), self.dest_entry.get(), weight="weight")
            new_cost = nx.shortest_path_length(self.graph, self.source_entry.get(), self.dest_entry.get(), weight="weight")
            
            if hasattr(self, "previous_best"):
                old_path, old_cost = self.previous_best
                self.display("\n--- Route Comparison ---")
                self.display("Before: " + " → ".join(old_path) + f" | Cost: {old_cost}")
                self.display("After: " + " → ".join(new_path) + f" | Cost: {new_cost}")
        except:
            self.display("No route available after failure")
        self.draw_graph()

    def reset_network(self):
        self.clear_output()

        self.network.reset_network()
        self.graph = self.network.graph
        self.routes = []
        self.display("Network reset successfully")
        self.draw_graph()


def main():
    root = tk.Tk()
    app = EmergencyNetworkSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()