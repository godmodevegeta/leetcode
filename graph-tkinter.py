import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import numpy as np
import json
import ast
from matplotlib.patches import FancyBboxPatch

class GraphVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Professional Graph Visualizer")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Accent.TButton', background='#4CAF50')
        style.configure('Danger.TButton', background='#f44336')
        style.configure('Info.TButton', background='#2196F3')
        
        # Variables
        self.graph = None
        self.figure = None
        self.canvas = None
        self.current_layout = 'spring'
        
        self.setup_ui()
        self.load_default_example()
        
    def setup_ui(self):
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for inputs and controls
        left_panel = ttk.Frame(main_container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Right panel for graph display
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.setup_input_panel(left_panel)
        self.setup_graph_panel(right_panel)
        
    def setup_input_panel(self, parent):
        # Input section
        input_frame = ttk.LabelFrame(parent, text="📊 Graph Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Number of nodes
        ttk.Label(input_frame, text="Number of nodes (n):").pack(anchor=tk.W)
        self.n_var = tk.StringVar(value="4")
        n_entry = ttk.Entry(input_frame, textvariable=self.n_var, width=30)
        n_entry.pack(fill=tk.X, pady=(2, 10))
        
        # Edges input
        ttk.Label(input_frame, text="Edges (JSON or line format):").pack(anchor=tk.W)
        self.edges_text = tk.Text(input_frame, height=8, width=35, font=('Consolas', 10))
        self.edges_text.pack(fill=tk.X, pady=(2, 10))
        
        # Scrollbar for edges text
        edges_scroll = ttk.Scrollbar(input_frame, orient="vertical", command=self.edges_text.yview)
        self.edges_text.configure(yscrollcommand=edges_scroll.set)
        
        # Action buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="🎨 Visualize", 
                  command=self.visualize_graph, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🗑️ Clear", 
                  command=self.clear_inputs,
                  style='Danger.TButton').pack(side=tk.LEFT, padx=5)
        
        # Examples section
        examples_frame = ttk.LabelFrame(parent, text="🎯 Quick Examples", padding=10)
        examples_frame.pack(fill=tk.X, pady=(0, 10))
        
        examples = [
            ("⭐ Star", self.load_star),
            ("🔄 Cycle", self.load_cycle), 
            ("🌳 Tree", self.load_tree),
            ("🔗 Complete", self.load_complete),
            ("➡️ Path", self.load_path),
            ("⏹️ Grid", self.load_grid),
            ("🎲 Random", self.load_random),
            ("💔 Disconnected", self.load_disconnected)
        ]
        
        for i, (name, command) in enumerate(examples):
            row = i // 2
            col = i % 2
            ttk.Button(examples_frame, text=name, command=command,
                      style='Info.TButton', width=12).grid(row=row, column=col, padx=2, pady=2)
        
        # Layout options
        layout_frame = ttk.LabelFrame(parent, text="🎨 Layout Options", padding=10)
        layout_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.layout_var = tk.StringVar(value="spring")
        layouts = [("Spring", "spring"), ("Circular", "circular"), ("Random", "random"), 
                  ("Shell", "shell"), ("Spectral", "spectral")]
        
        for text, value in layouts:
            ttk.Radiobutton(layout_frame, text=text, variable=self.layout_var, 
                           value=value, command=self.update_layout).pack(anchor=tk.W)
        
        # Graph info section
        self.info_frame = ttk.LabelFrame(parent, text="📈 Graph Statistics", padding=10)
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        
        self.info_text = tk.Text(self.info_frame, height=10, font=('Consolas', 9), 
                                state=tk.DISABLED, wrap=tk.WORD)
        info_scroll = ttk.Scrollbar(self.info_frame, orient="vertical", command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=info_scroll.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        info_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
    def setup_graph_panel(self, parent):
        # Graph display frame
        graph_frame = ttk.LabelFrame(parent, text="🌐 Graph Visualization", padding=5)
        graph_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(8, 6), facecolor='white')
        self.figure.patch.set_facecolor('#f8f9fa')
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, graph_frame)
        toolbar.update()
        
    def parse_edges_input(self):
        """Parse edges from text input"""
        text = self.edges_text.get(1.0, tk.END).strip()
        if not text:
            return []
            
        # Try JSON format first
        if text.startswith('['):
            try:
                return ast.literal_eval(text)
            except:
                raise ValueError("Invalid JSON format for edges")
        
        # Parse line by line
        edges = []
        for line in text.split('\n'):
            line = line.strip()
            if line:
                parts = line.split()
                if len(parts) == 2:
                    try:
                        a, b = int(parts[0]), int(parts[1])
                        edges.append([a, b])
                    except ValueError:
                        raise ValueError(f"Invalid edge format: {line}")
                else:
                    raise ValueError(f"Each line must have exactly 2 numbers: {line}")
        return edges
    
    def validate_inputs(self):
        """Validate all inputs"""
        try:
            n = int(self.n_var.get())
            if n < 1 or n > 1000:
                raise ValueError("Number of nodes must be between 1 and 1000")
            
            edges = self.parse_edges_input()
            
            # Validate edge nodes
            for edge in edges:
                if len(edge) != 2:
                    raise ValueError(f"Edge {edge} must have exactly 2 nodes")
                a, b = edge
                if not (0 <= a < n and 0 <= b < n):
                    raise ValueError(f"Edge [{a},{b}] contains nodes outside range 0-{n-1}")
            
            return n, edges
        except Exception as e:
            messagebox.showerror("Input Error", str(e))
            return None, None
    
    def visualize_graph(self):
        """Main visualization function"""
        n, edges = self.validate_inputs()
        if n is None:
            return
        
        # Create NetworkX graph
        self.graph = nx.Graph()
        self.graph.add_nodes_from(range(n))
        self.graph.add_edges_from(edges)
        
        self.draw_graph()
        self.update_info()
    
    def draw_graph(self):
        """Draw the graph with current layout"""
        if self.graph is None:
            return
        
        self.ax.clear()
        
        # Choose layout
        layout_func = {
            'spring': lambda G: nx.spring_layout(G, k=1, iterations=50),
            'circular': nx.circular_layout,
            'random': nx.random_layout,
            'shell': nx.shell_layout,
            'spectral': nx.spectral_layout
        }
        
        try:
            pos = layout_func[self.layout_var.get()](self.graph)
        except:
            pos = nx.spring_layout(self.graph, k=1, iterations=50)
        
        n = self.graph.number_of_nodes()
        
        # Draw edges
        nx.draw_networkx_edges(self.graph, pos, ax=self.ax, 
                              edge_color='#666666', alpha=0.6, width=2)
        
        # Color nodes based on degree
        node_colors = []
        degrees = dict(self.graph.degree())
        max_degree = max(degrees.values()) if degrees else 1
        
        for node in self.graph.nodes():
            degree = degrees[node]
            if degree == 0:
                node_colors.append('#ff5252')  # Red for isolated
            elif degree == max_degree:
                node_colors.append('#4CAF50')  # Green for highest degree
            else:
                # Gradient from yellow to green based on degree
                intensity = degree / max_degree
                node_colors.append(plt.cm.YlGn(0.3 + 0.7 * intensity))
        
        # Draw nodes
        node_size = max(300, 3000 // n) if n <= 50 else max(100, 1500 // n)
        nx.draw_networkx_nodes(self.graph, pos, ax=self.ax,
                              node_color=node_colors, node_size=node_size,
                              alpha=0.8, edgecolors='black', linewidths=1)
        
        # Draw labels
        if n <= 50:
            font_size = max(8, 16 - n // 5)
            nx.draw_networkx_labels(self.graph, pos, ax=self.ax, 
                                   font_size=font_size, font_weight='bold')
        
        # Title and styling
        self.ax.set_title(f'Graph with {n} nodes and {self.graph.number_of_edges()} edges\n'
                         f'Layout: {self.layout_var.get().title()}', 
                         fontsize=14, fontweight='bold', pad=20)
        self.ax.axis('off')
        
        # Add legend
        if n > 0:
            legend_elements = [
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#ff5252', 
                          markersize=10, label='Isolated nodes'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4CAF50', 
                          markersize=10, label='Highest degree'),
                plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FFF176', 
                          markersize=10, label='Other nodes')
            ]
            self.ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))
        
        plt.tight_layout()
        self.canvas.draw()
    
    def update_layout(self):
        """Update graph layout"""
        if self.graph is not None:
            self.draw_graph()
    
    def update_info(self):
        """Update graph information display"""
        if self.graph is None:
            return
        
        G = self.graph
        
        # Basic stats
        info = []
        info.append("=== BASIC STATISTICS ===")
        info.append(f"Nodes: {G.number_of_nodes()}")
        info.append(f"Edges: {G.number_of_edges()}")
        info.append(f"Density: {nx.density(G):.3f}")
        info.append(f"Connected: {'Yes' if nx.is_connected(G) else 'No'}")
        info.append(f"Connected Components: {nx.number_connected_components(G)}")
        info.append("")
        
        # Degree statistics
        degrees = dict(G.degree())
        if degrees:
            degree_values = list(degrees.values())
            info.append("=== DEGREE STATISTICS ===")
            info.append(f"Max Degree: {max(degree_values)}")
            info.append(f"Min Degree: {min(degree_values)}")
            info.append(f"Avg Degree: {np.mean(degree_values):.2f}")
            info.append(f"Degree Variance: {np.var(degree_values):.2f}")
            info.append("")
            
            # Node degrees
            info.append("=== NODE DEGREES ===")
            sorted_degrees = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
            for node, degree in sorted_degrees[:20]:  # Show top 20
                info.append(f"Node {node}: {degree}")
            if len(sorted_degrees) > 20:
                info.append(f"... and {len(sorted_degrees) - 20} more nodes")
        
        # Advanced metrics for connected graphs
        if nx.is_connected(G) and G.number_of_nodes() > 1:
            info.append("\n=== ADVANCED METRICS ===")
            try:
                info.append(f"Diameter: {nx.diameter(G)}")
                info.append(f"Radius: {nx.radius(G)}")
                info.append(f"Average Clustering: {nx.average_clustering(G):.3f}")
                if G.number_of_nodes() <= 100:  # Only for smaller graphs
                    avg_path_length = nx.average_shortest_path_length(G)
                    info.append(f"Avg Path Length: {avg_path_length:.3f}")
            except:
                pass
        
        # Update text widget
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, '\n'.join(info))
        self.info_text.config(state=tk.DISABLED)
    
    def clear_inputs(self):
        """Clear all inputs"""
        self.n_var.set("")
        self.edges_text.delete(1.0, tk.END)
        if self.ax:
            self.ax.clear()
            self.canvas.draw()
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.graph = None
    
    # Example loading methods
    def load_default_example(self):
        self.n_var.set("4")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "[[1,0],[1,2],[1,3]]")
        self.visualize_graph()
    
    def load_star(self):
        self.n_var.set("6")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "0 1\n0 2\n0 3\n0 4\n0 5")
        self.visualize_graph()
    
    def load_cycle(self):
        self.n_var.set("6")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "0 1\n1 2\n2 3\n3 4\n4 5\n5 0")
        self.visualize_graph()
    
    def load_tree(self):
        self.n_var.set("10")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "0 1\n0 2\n1 3\n1 4\n2 5\n2 6\n3 7\n3 8\n4 9")
        self.visualize_graph()
    
    def load_complete(self):
        n = 5
        self.n_var.set(str(n))
        edges = []
        for i in range(n):
            for j in range(i+1, n):
                edges.append([i, j])
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, str(edges))
        self.visualize_graph()
    
    def load_path(self):
        self.n_var.set("8")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7")
        self.visualize_graph()
    
    def load_grid(self):
        self.n_var.set("9")
        edges = []
        # 3x3 grid
        for i in range(3):
            for j in range(3):
                curr = i*3 + j
                if j < 2: edges.append([curr, curr+1])  # right
                if i < 2: edges.append([curr, curr+3])  # down
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, '\n'.join([f"{e[0]} {e[1]}" for e in edges]))
        self.visualize_graph()
    
    def load_random(self):
        import random
        n = random.randint(6, 12)
        self.n_var.set(str(n))
        num_edges = random.randint(n-1, n*(n-1)//4)
        edges = set()
        while len(edges) < num_edges:
            a, b = random.randint(0, n-1), random.randint(0, n-1)
            if a != b:
                edges.add((min(a, b), max(a, b)))
        
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, str([list(e) for e in edges]))
        self.visualize_graph()
    
    def load_disconnected(self):
        self.n_var.set("8")
        self.edges_text.delete(1.0, tk.END)
        self.edges_text.insert(1.0, "0 1\n1 2\n4 5\n5 6\n6 4")  # Two components + isolated nodes
        self.visualize_graph()

def main():
    try:
        root = tk.Tk()
        app = GraphVisualizer(root)
        
        # Center window
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (root.winfo_screenheight() // 2) - (800 // 2)
        root.geometry(f'1200x800+{x}+{y}')
        
        root.mainloop()
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Make sure you have tkinter installed:")
        print("brew install python-tk")

if __name__ == "__main__":
    main()