from algorithm import safest_path_maxmin, merge_sort, binary_search
import tkinter as tk
from tkinter import ttk, scrolledtext
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class EmergencyNetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Routing Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.setup_styles()
        self.create_ui()
        self.create_sample_graph()
        self.update_status("Ready")

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

    def create_ui(self):
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(title_frame, text="🚨 Emergency Network Routing Simulator",
                 font=('Arial', 20, 'bold'),
                 bg="#2c3e50", fg="white").pack(pady=15)

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
        frame = tk.LabelFrame(parent, text="📝 Network Parameters",
                              font=('Arial', 11, 'bold'),
                              bg="#ecf0f1", padx=10, pady=10)
        frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame, text="Source:").grid(row=0, column=0)
        self.source_entry = tk.Entry(frame)
        self.source_entry.grid(row=0, column=1)
        self.source_entry.insert(0, "A")

        tk.Label(frame, text="Destination:").grid(row=1, column=0)
        self.dest_entry = tk.Entry(frame)
        self.dest_entry.grid(row=1, column=1)
        self.dest_entry.insert(0, "F")

        # ✅ Added search input (minimal UI change)
        tk.Label(frame, text="Search Route:").grid(row=2, column=0)
        self.search_entry = tk.Entry(frame)
        self.search_entry.grid(row=2, column=1)

    def create_button_section(self, parent):
        frame = tk.LabelFrame(parent, text="⚡ Operations",
                              font=('Arial', 11, 'bold'),
                              bg="#ecf0f1", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, padx=10, pady=10)

        buttons = [
            ("Generate Routes", self.generate_routes),
            ("Find Best Route", self.find_best_route),
            ("Sort Routes", self.sort_routes),
            ("Find Safest Route", self.find_safest_route),
            ("Search Route", self.search_route)  # ✅ added
        ]

        for text, cmd in buttons:
            tk.Button(frame, text=text, command=cmd).pack(fill=tk.X, pady=5)

    def create_output_section(self, parent):
        frame = tk.LabelFrame(parent, text="Output")
        frame.pack(fill=tk.BOTH, expand=True)

        self.output = scrolledtext.ScrolledText(frame)
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

    def create_sample_graph(self):
        G = nx.Graph()
        edges = [
            ('A', 'B', 4), ('A', 'C', 2),
            ('B', 'D', 5), ('C', 'D', 8),
            ('D', 'F', 6), ('C', 'E', 10),
            ('E', 'F', 3)
        ]
        G.add_weighted_edges_from(edges)
        self.graph = G
        self.draw_graph()

    def draw_graph(self, highlight=None):
        self.ax.clear()
        pos = nx.spring_layout(self.graph)

        nx.draw(self.graph, pos, ax=self.ax, with_labels=True)

        if highlight:
            edges = list(zip(highlight[:-1], highlight[1:]))
            nx.draw_networkx_edges(self.graph, pos, edgelist=edges,
                                   edge_color='r', width=3, ax=self.ax)

        self.canvas.draw()

    # ---------------- BUTTON FUNCTIONS ----------------

    def generate_routes(self):
        self.clear_output()

        source = self.source_entry.get()
        dest = self.dest_entry.get()

        try:
            paths = list(nx.all_simple_paths(self.graph, source, dest))
            self.routes = []

            for path in paths:
                dist = sum(self.graph[path[i]][path[i+1]]['weight']
                           for i in range(len(path)-1))
                route_str = " → ".join(path)
                self.routes.append((route_str, dist))

            self.display("Generated Routes:\n")
            for r, d in self.routes:
                self.display(f"{r} | {d}")

        except:
            self.display("Invalid nodes")

    def find_best_route(self):
        self.clear_output()

        try:
            path = nx.shortest_path(
                self.graph,
                self.source_entry.get(),
                self.dest_entry.get(),
                weight='weight'
            )
            self.display("Best: " + " → ".join(path))
            self.draw_graph(path)
        except:
            self.display("No path")

    def sort_routes(self):
        self.clear_output()

        if not hasattr(self, 'routes'):
            self.display("Generate routes first")
            return

        self.routes = merge_sort(self.routes)

        self.display("Sorted Routes:\n")
        for r, d in self.routes:
            self.display(f"{r} | {d}")

    def find_safest_route(self):
        self.clear_output()

        source = self.source_entry.get()
        dest = self.dest_entry.get()

        path, cap = safest_path_maxmin(self.graph, source, dest)

        if path:
            self.display("Safest: " + " → ".join(path))
            self.display(f"Min Capacity: {cap}")
            self.draw_graph(path)
        else:
            self.display("No safe route")

    def search_route(self):
        self.clear_output()

        if not hasattr(self, 'routes'):
            self.display("Generate routes first")
            return

        target = self.search_entry.get().strip()

        result = binary_search(self.routes, target)

        if result:
            self.display(f"Found: {result[0]} | {result[1]}")
        else:
            self.display("Route not found")


def main():
    root = tk.Tk()
    app = EmergencyNetworkSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()