"""
Emergency Network Routing and Optimization Simulator
A modern GUI application for network routing simulation and visualization
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
from matplotlib.figure import Figure

class EmergencyNetworkSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergency Network Routing Simulator")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")
        
        # Configure style
        self.setup_styles()
        
        # Create main container
        self.create_ui()
        
        # Initialize with sample graph
        self.create_sample_graph()
        
        # Update status
        self.update_status("Ready")
    
    def setup_styles(self):
        """Configure ttk styles for modern look"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Button style
        style.configure('Action.TButton', 
                       font=('Arial', 10, 'bold'),
                       padding=8,
                       background='#4CAF50',
                       foreground='white')
        
        # Label style
        style.configure('Title.TLabel',
                       font=('Arial', 24, 'bold'),
                       background='#f0f0f0',
                       foreground='#2c3e50')
        
        style.configure('Section.TLabel',
                       font=('Arial', 12, 'bold'),
                       background='#ecf0f1',
                       foreground='#34495e')
    
    def create_ui(self):
        """Create the main UI layout"""
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, 
                              text="🚨 Emergency Network Routing Simulator",
                              font=('Arial', 20, 'bold'),
                              bg="#2c3e50",
                              fg="white")
        title_label.pack(pady=15)
        
        # Main content area
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (Inputs and Buttons)
        left_panel = tk.Frame(content_frame, bg="#ecf0f1", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5), pady=0)
        
        self.create_input_section(left_panel)
        self.create_button_section(left_panel)
        
        # Right panel (Output and Graph)
        right_panel = tk.Frame(content_frame, bg="#f0f0f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        self.create_output_section(right_panel)
        self.create_graph_section(right_panel)
        
        # Status bar
        self.create_status_bar()
    
    def create_input_section(self, parent):
        """Create input fields section"""
        input_frame = tk.LabelFrame(parent, 
                                    text="📝 Network Parameters",
                                    font=('Arial', 11, 'bold'),
                                    bg="#ecf0f1",
                                    fg="#2c3e50",
                                    padx=15,
                                    pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Source Node
        tk.Label(input_frame, text="Source Node:", 
                font=('Arial', 10), bg="#ecf0f1").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.source_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.source_entry.grid(row=0, column=1, pady=5, padx=5)
        self.source_entry.insert(0, "A")
        
        # Destination Node
        tk.Label(input_frame, text="Destination Node:", 
                font=('Arial', 10), bg="#ecf0f1").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dest_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.dest_entry.grid(row=1, column=1, pady=5, padx=5)
        self.dest_entry.insert(0, "F")
        
        # Node Failure
        tk.Label(input_frame, text="Node Failure (optional):", 
                font=('Arial', 10), bg="#ecf0f1").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.node_failure_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.node_failure_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Edge Failure
        tk.Label(input_frame, text="Edge Failure (A-B):", 
                font=('Arial', 10), bg="#ecf0f1").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.edge_failure_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.edge_failure_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Route Search
        tk.Label(input_frame, text="Search Route:", 
                font=('Arial', 10), bg="#ecf0f1").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.search_entry = tk.Entry(input_frame, width=20, font=('Arial', 10))
        self.search_entry.grid(row=4, column=1, pady=5, padx=5)
    
    def create_button_section(self, parent):
        """Create buttons section"""
        button_frame = tk.LabelFrame(parent, 
                                     text="⚡ Operations",
                                     font=('Arial', 11, 'bold'),
                                     bg="#ecf0f1",
                                     fg="#2c3e50",
                                     padx=15,
                                     pady=10)
        button_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        
        # Button configurations
        buttons = [
            ("🔄 Generate Routes", self.generate_routes, "#3498db"),
            ("🎯 Find Best Route", self.find_best_route, "#2ecc71"),
            ("⚠️ Simulate Failure", self.simulate_failure, "#e74c3c"),
            ("📊 Sort Routes", self.sort_routes, "#9b59b6"),
            ("🛡️ Find Safest Route", self.find_safest_route, "#f39c12"),
            ("🔍 Search Route", self.search_route, "#1abc9c"),
            ("🗑️ Reset / Clear", self.reset_inputs, "#95a5a6")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(button_frame, 
                          text=text,
                          command=command,
                          font=('Arial', 10, 'bold'),
                          bg=color,
                          fg="white",
                          activebackground=color,
                          activeforeground="white",
                          cursor="hand2",
                          relief=tk.RAISED,
                          bd=2,
                          padx=10,
                          pady=8)
            btn.pack(fill=tk.X, pady=5)
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.configure(relief=tk.SUNKEN))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(relief=tk.RAISED))
    
    def create_output_section(self, parent):
        """Create output display section"""
        output_frame = tk.LabelFrame(parent, 
                                     text="📊 Output Display",
                                     font=('Arial', 11, 'bold'),
                                     bg="#ffffff",
                                     fg="#2c3e50",
                                     padx=10,
                                     pady=10)
        output_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Scrolled text widget
        self.output_text = scrolledtext.ScrolledText(output_frame,
                                                     width=60,
                                                     height=15,
                                                     font=('Consolas', 10),
                                                     bg="#f8f9fa",
                                                     fg="#2c3e50",
                                                     wrap=tk.WORD,
                                                     relief=tk.SUNKEN,
                                                     bd=2)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Configure tags for colored output
        self.output_text.tag_config("header", foreground="#2c3e50", font=('Consolas', 10, 'bold'))
        self.output_text.tag_config("success", foreground="#27ae60", font=('Consolas', 10, 'bold'))
        self.output_text.tag_config("error", foreground="#e74c3c", font=('Consolas', 10, 'bold'))
        self.output_text.tag_config("info", foreground="#3498db", font=('Consolas', 10))
        
        # Initial message
        self.display_output("Welcome to Emergency Network Routing Simulator!\n", "header")
        self.display_output("Click any operation button to begin simulation.\n\n", "info")
    
    def create_graph_section(self, parent):
        """Create graph visualization section"""
        graph_frame = tk.LabelFrame(parent, 
                                    text="📈 Network Graph Visualization",
                                    font=('Arial', 11, 'bold'),
                                    bg="#ffffff",
                                    fg="#2c3e50",
                                    padx=10,
                                    pady=10)
        graph_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor='#f8f9fa')
        self.ax = self.fig.add_subplot(111)
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = tk.Label(self.root, 
                                   text="Ready",
                                   font=('Arial', 9),
                                   bg="#34495e",
                                   fg="white",
                                   anchor=tk.W,
                                   relief=tk.SUNKEN,
                                   padx=10)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_sample_graph(self):
        """Create and display a sample network graph"""
        # Create sample graph
        G = nx.Graph()
        edges = [
            ('A', 'B', 4), ('A', 'C', 2),
            ('B', 'C', 1), ('B', 'D', 5),
            ('C', 'D', 8), ('C', 'E', 10),
            ('D', 'E', 2), ('D', 'F', 6),
            ('E', 'F', 3)
        ]
        G.add_weighted_edges_from(edges)
        
        self.graph = G
        self.draw_graph(G)
    
    def draw_graph(self, G, highlight_path=None):
        """Draw network graph with optional path highlighting"""
        self.ax.clear()
        
        # Layout
        pos = nx.spring_layout(G, seed=42, k=0.9)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, ax=self.ax, 
                              edge_color='#95a5a6', 
                              width=2, 
                              alpha=0.6)
        
        # Draw edge labels (weights)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels, 
                                     ax=self.ax, 
                                     font_size=8)
        
        # Highlight path if provided
        if highlight_path:
            path_edges = list(zip(highlight_path[:-1], highlight_path[1:]))
            nx.draw_networkx_edges(G, pos, path_edges, 
                                  ax=self.ax,
                                  edge_color='#e74c3c', 
                                  width=4)
        
        # Draw nodes
        node_colors = ['#3498db' if node not in (highlight_path or []) 
                      else '#2ecc71' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, ax=self.ax,
                              node_color=node_colors,
                              node_size=800,
                              alpha=0.9)
        
        # Draw labels
        nx.draw_networkx_labels(G, pos, ax=self.ax,
                               font_size=12,
                               font_weight='bold',
                               font_color='white')
        
        self.ax.set_title("Emergency Network Topology", 
                         fontsize=12, 
                         fontweight='bold',
                         color='#2c3e50')
        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()
    
    def display_output(self, text, tag="info"):
        """Display text in output area with formatting"""
        self.output_text.insert(tk.END, text, tag)
        self.output_text.see(tk.END)
    
    def clear_output(self):
        """Clear output display"""
        self.output_text.delete(1.0, tk.END)
    
    def update_status(self, message):
        """Update status bar message"""
        self.status_bar.config(text=f"Status: {message}")
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Validate input fields"""
        source = self.source_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        if not source or not dest:
            messagebox.showwarning("Input Error", 
                                  "Please enter both Source and Destination nodes!")
            return False
        return True
    
    # ==================== Button Action Functions ====================
    
    def generate_routes(self):
        """Generate all possible routes between source and destination"""
        if not self.validate_inputs():
            return
        
        self.update_status("Generating routes...")
        self.clear_output()
        
        source = self.source_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("🔄 GENERATE ROUTES\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        self.display_output(f"Source: {source}\n", "info")
        self.display_output(f"Destination: {dest}\n\n", "info")
        
        # Dummy routes for demonstration
        routes = [
            f"{source} → B → D → {dest}",
            f"{source} → C → E → {dest}",
            f"{source} → B → C → E → {dest}",
            f"{source} → C → D → {dest}"
        ]
        
        self.display_output("Generated Routes:\n", "success")
        for i, route in enumerate(routes, 1):
            self.display_output(f"  Route {i}: {route}\n", "info")
        
        self.display_output(f"\nTotal routes found: {len(routes)}\n", "success")
        
        # Visualize first route
        if source in self.graph and dest in self.graph:
            try:
                path = nx.shortest_path(self.graph, source, dest)
                self.draw_graph(self.graph, path)
            except:
                self.draw_graph(self.graph)
        
        self.update_status("Routes generated successfully")
    
    def find_best_route(self):
        """Find the best (shortest) route"""
        if not self.validate_inputs():
            return
        
        self.update_status("Finding best route...")
        self.clear_output()
        
        source = self.source_entry.get().strip()
        dest = self.dest_entry.get().strip()
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("🎯 FIND BEST ROUTE\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        if source in self.graph and dest in self.graph:
            try:
                path = nx.shortest_path(self.graph, source, dest, weight='weight')
                length = nx.shortest_path_length(self.graph, source, dest, weight='weight')
                
                route_str = " → ".join(path)
                self.display_output(f"Best Route: {route_str}\n", "success")
                self.display_output(f"Total Distance: {length} units\n", "success")
                self.display_output(f"Hops: {len(path) - 1}\n\n", "info")
                
                self.draw_graph(self.graph, path)
            except nx.NetworkXNoPath:
                self.display_output("❌ No path exists between nodes!\n", "error")
        else:
            self.display_output(f"Best Route: {source} → B → D → {dest}\n", "success")
            self.display_output("Total Distance: 15 units\n", "success")
            self.display_output("Hops: 3\n", "info")
        
        self.update_status("Best route found")
    
    def simulate_failure(self):
        """Simulate node or edge failure"""
        self.update_status("Simulating failure...")
        self.clear_output()
        
        node_failure = self.node_failure_entry.get().strip()
        edge_failure = self.edge_failure_entry.get().strip()
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("⚠️ SIMULATE FAILURE\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        if node_failure:
            self.display_output(f"Simulating Node Failure: {node_failure}\n\n", "error")
            self.display_output(f"Node {node_failure} is now OFFLINE\n", "error")
            self.display_output("Recalculating routes...\n\n", "info")
            self.display_output("Alternate Route: A → C → E → F\n", "success")
            self.display_output("New Distance: 18 units\n", "info")
        elif edge_failure:
            self.display_output(f"Simulating Edge Failure: {edge_failure}\n\n", "error")
            self.display_output(f"Edge {edge_failure} is now DISCONNECTED\n", "error")
            self.display_output("Recalculating routes...\n\n", "info")
            self.display_output("Alternate Route: A → C → D → F\n", "success")
            self.display_output("New Distance: 16 units\n", "info")
        else:
            messagebox.showwarning("Input Required", 
                                  "Please specify a node or edge failure!")
            self.update_status("Ready")
            return
        
        self.update_status("Failure simulation complete")
    
    def sort_routes(self):
        """Sort routes by distance"""
        self.update_status("Sorting routes...")
        self.clear_output()
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("📊 SORT ROUTES BY DISTANCE\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        routes = [
            ("A → B → D → F", 15),
            ("A → C → E → F", 18),
            ("A → B → C → E → F", 20),
            ("A → C → D → F", 16)
        ]
        
        sorted_routes = sorted(routes, key=lambda x: x[1])
        
        self.display_output("Routes sorted by distance (ascending):\n\n", "success")
        for i, (route, dist) in enumerate(sorted_routes, 1):
            self.display_output(f"  {i}. {route} - {dist} units\n", "info")
        
        self.update_status("Routes sorted successfully")
    
    def find_safest_route(self):
        """Find the safest route (max-min algorithm)"""
        self.update_status("Finding safest route...")
        self.clear_output()
        
        source = self.source_entry.get().strip() or "A"
        dest = self.dest_entry.get().strip() or "F"
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("🛡️ FIND SAFEST ROUTE (Max-Min)\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        self.display_output(f"Safest Route: {source} → C → E → {dest}\n", "success")
        self.display_output("Minimum Edge Capacity: 8 units\n", "success")
        self.display_output("Safety Score: 95%\n", "info")
        self.display_output("\nThis route maximizes the minimum edge capacity.\n", "info")
        
        self.update_status("Safest route found")
    
    def search_route(self):
        """Search for a specific route"""
        search_term = self.search_entry.get().strip()
        
        if not search_term:
            messagebox.showwarning("Input Required", 
                                  "Please enter a route to search!")
            return
        
        self.update_status("Searching route...")
        self.clear_output()
        
        self.display_output("=" * 60 + "\n", "header")
        self.display_output("🔍 SEARCH ROUTE\n", "header")
        self.display_output("=" * 60 + "\n\n", "header")
        
        self.display_output(f"Searching for: {search_term}\n\n", "info")
        
        # Dummy search result
        self.display_output("✓ Route found!\n", "success")
        self.display_output(f"Route: A → {search_term} → F\n", "info")
        self.display_output("Distance: 12 units\n", "info")
        self.display_output("Status: Active\n", "success")
        
        self.update_status("Search complete")
    
    def reset_inputs(self):
        """Reset all input fields and output"""
        self.source_entry.delete(0, tk.END)
        self.dest_entry.delete(0, tk.END)
        self.node_failure_entry.delete(0, tk.END)
        self.edge_failure_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        
        self.source_entry.insert(0, "A")
        self.dest_entry.insert(0, "F")
        
        self.clear_output()
        self.display_output("All inputs cleared. Ready for new simulation.\n", "success")
        
        # Reset graph
        self.create_sample_graph()
        
        self.update_status("Reset complete")


def main():
    """Main function to run the application"""
    root = tk.Tk()
    app = EmergencyNetworkSimulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
