import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import math
import ast

class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualizer")
        self.root.geometry("800x700")
        
        # Variables
        self.n = 0
        self.edges = []
        self.graph = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Graph Input", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Number of nodes input
        ttk.Label(input_frame, text="Number of nodes (n):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.n_entry = ttk.Entry(input_frame, width=10)
        self.n_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.n_entry.insert(0, "4")
        
        # Edges input
        ttk.Label(input_frame, text="Edges (format: [[1,0],[1,2],[1,3]]):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.edges_entry = ttk.Entry(input_frame, width=50)
        self.edges_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=2)
        self.edges_entry.insert(0, "[[1,0],[1,2],[1,3]]")
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(button_frame, text="Visualize Graph", command=self.visualize_graph).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Clear", command=self.clear_inputs).pack(side=tk.LEFT, padx=5)
        
        # Graph display area
        self.canvas_frame = ttk.LabelFrame(main_frame, text="Graph Visualization", padding="5")
        self.canvas_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Info section
        info_frame = ttk.LabelFrame(main_frame, text="Graph Information", padding="10")
        info_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        self.info_text = tk.Text(info_frame, height=4, width=70)
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        input_frame.columnconfigure(1, weight=1)
        self.canvas_frame.columnconfigure(0, weight=1)
        self.canvas_frame.rowconfigure(0, weight=1)
        info_frame.columnconfigure(0, weight=1)
        
    def parse_inputs(self):
        """Parse and validate inputs"""
        try:
            # Parse n
            n = int(self.n_entry.get())
            if n < 1 or n > 20000:
                raise ValueError("Number of nodes must be between 1 and 20,000")
            
            # Parse edges
            edges_str = self.edges_entry.get().strip()
            if edges_str:
                edges = ast.literal_eval(edges_str)
                if not isinstance(edges, list):
                    raise ValueError("Edges must be a list")
                
                # Validate edges
                for edge in edges:
                    if not isinstance(edge, list) or len(edge) != 2:
                        raise ValueError("Each edge must be a list of two nodes")
                    a, b = edge
                    if not (0 <= a < n and 0 <= b < n):
                        raise ValueError(f"Edge nodes must be between 0 and {n-1}")
            else:
                edges = []
            
            return n, edges
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
            return None, None
        except Exception as e:
            messagebox.showerror("Parse Error", f"Error parsing inputs: {str(e)}")
            return None, None
    
    def create_graph_info(self, G):
        """Generate information about the graph"""
        info = []
        info.append(f"Nodes: {G.number_of_nodes()}")
        info.append(f"Edges: {G.number_of_edges()}")
        info.append(f"Connected Components: {nx.number_connected_components(G)}")
        
        # Degree information
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees else 0
        min_degree = min(degrees.values()) if degrees else 0
        avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
        
        info.append(f"Degree - Min: {min_degree}, Max: {max_degree}, Avg: {avg_degree:.2f}")
        
        # List nodes with their degrees
        degree_info = ", ".join([f"{node}({deg})" for node, deg in sorted(degrees.items())])
        info.append(f"Node degrees: {degree_info}")
        
        return "\n".join(info)
    
    def visualize_graph(self):
        """Create and display the graph visualization"""
        n, edges = self.parse_inputs()
        if n is None or edges is None:
            return
        
        # Clear previous canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Create NetworkX graph
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor('white')
        
        # Choose layout based on graph size
        if n <= 20:
            pos = nx.spring_layout(G, k=2, iterations=50)
        elif n <= 100:
            pos = nx.spring_layout(G, k=1, iterations=30)
        else:
            pos = nx.spring_layout(G, k=0.5, iterations=20)
        
        # Draw the graph
        # Draw edges first
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.6, width=1)
        
        # Draw nodes
        node_colors = ['lightblue' if G.degree(node) > 0 else 'lightcoral' for node in G.nodes()]
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, 
                              node_size=300 if n <= 50 else 100, alpha=0.8)
        
        # Draw labels
        if n <= 100:  # Only show labels for smaller graphs
            nx.draw_networkx_labels(G, pos, ax=ax, font_size=8 if n <= 50 else 6)
        
        ax.set_title(f"Graph with {n} nodes and {len(edges)} edges", fontsize=12, fontweight='bold')
        ax.axis('off')
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Update info
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, self.create_graph_info(G))
        
        # Store graph for potential future use
        self.graph = G
        self.n = n
        self.edges = edges
        
    def clear_inputs(self):
        """Clear all inputs and visualization"""
        self.n_entry.delete(0, tk.END)
        self.edges_entry.delete(0, tk.END)
        self.info_text.delete(1.0, tk.END)
        
        # Clear canvas
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

def main():
    root = tk.Tk()
    app = GraphVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()