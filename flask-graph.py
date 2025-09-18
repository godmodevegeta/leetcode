from flask import Flask, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Graph Visualizer</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f0f0f0;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .input-section {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .input-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            border: 2px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
            box-sizing: border-box;
        }
        textarea {
            height: 100px;
            font-family: monospace;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 5px;
        }
        button:hover {
            background-color: #45a049;
        }
        .clear-btn {
            background-color: #f44336;
        }
        .clear-btn:hover {
            background-color: #da190b;
        }
        .example-btn {
            background-color: #2196F3;
            font-size: 12px;
            padding: 5px 10px;
        }
        .example-btn:hover {
            background-color: #1976D2;
        }
        #graph-container {
            border: 2px solid #ddd;
            border-radius: 8px;
            margin: 20px 0;
            background: white;
        }
        #graph {
            width: 100%;
            height: 500px;
        }
        .info-section {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
        .node {
            stroke: #333;
            stroke-width: 2px;
            cursor: pointer;
        }
        .link {
            stroke: #666;
            stroke-width: 2px;
        }
        .node-label {
            font-size: 12px;
            font-weight: bold;
            text-anchor: middle;
            pointer-events: none;
            fill: #333;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌐 Graph Visualizer</h1>
        
        <div class="input-section">
            <div class="input-group">
                <label>Number of nodes (n):</label>
                <input type="number" id="n-input" value="4" min="1" max="100">
            </div>
            
            <div class="input-group">
                <label>Edges (one per line: "1 0" or JSON format: [[1,0],[1,2]]):</label>
                <textarea id="edges-input" placeholder="Enter edges like:
1 0
1 2
1 3

Or JSON format: [[1,0],[1,2],[1,3]]">1 0
1 2
1 3</textarea>
            </div>
            
            <div>
                <button onclick="visualizeGraph()">🎨 Visualize Graph</button>
                <button class="clear-btn" onclick="clearAll()">🗑️ Clear</button>
            </div>
            
            <div style="margin-top: 15px;">
                <strong>Quick Examples:</strong><br>
                <button class="example-btn" onclick="loadExample('star')">⭐ Star</button>
                <button class="example-btn" onclick="loadExample('cycle')">🔄 Cycle</button>
                <button class="example-btn" onclick="loadExample('tree')">🌳 Tree</button>
                <button class="example-btn" onclick="loadExample('complete')">🔗 Complete</button>
                <button class="example-btn" onclick="loadExample('path')">➡️ Path</button>
                <button class="example-btn" onclick="loadExample('grid')">⏹️ Grid</button>
            </div>
        </div>
        
        <div id="error-container"></div>
        
        <div id="graph-container">
            <svg id="graph"></svg>
        </div>
        
        <div id="info-section" class="info-section" style="display: none;">
            <h3>📊 Graph Information:</h3>
            <div id="graph-info"></div>
        </div>
    </div>

    <script>
        let simulation;
        
        function showError(message) {
            const container = document.getElementById('error-container');
            container.innerHTML = '<div class="error">❌ ' + message + '</div>';
        }
        
        function clearError() {
            document.getElementById('error-container').innerHTML = '';
        }
        
        function parseEdges(edgesStr) {
            edgesStr = edgesStr.trim();
            if (!edgesStr) return [];
            
            // Try JSON format first
            if (edgesStr.startsWith('[')) {
                try {
                    return JSON.parse(edgesStr);
                } catch (e) {
                    throw new Error('Invalid JSON format');
                }
            }
            
            // Parse line by line format
            const lines = edgesStr.split('\n').filter(line => line.trim());
            const edges = [];
            
            for (let line of lines) {
                const parts = line.trim().split(/\s+/);
                if (parts.length === 2) {
                    const a = parseInt(parts[0]);
                    const b = parseInt(parts[1]);
                    if (!isNaN(a) && !isNaN(b)) {
                        edges.push([a, b]);
                    }
                }
            }
            
            return edges;
        }
        
        function visualizeGraph() {
            clearError();
            
            try {
                const n = parseInt(document.getElementById('n-input').value);
                const edgesStr = document.getElementById('edges-input').value;
                
                if (n < 1 || n > 100) {
                    throw new Error('Number of nodes must be between 1 and 100');
                }
                
                const edges = parseEdges(edgesStr);
                
                // Validate edges
                for (let edge of edges) {
                    if (edge[0] >= n || edge[1] >= n || edge[0] < 0 || edge[1] < 0) {
                        throw new Error('Edge [' + edge[0] + ',' + edge[1] + '] is outside node range 0-' + (n-1));
                    }
                }
                
                drawGraph(n, edges);
                
            } catch (e) {
                showError(e.message);
            }
        }
        
        function drawGraph(n, edges) {
            // Clear previous graph
            d3.select("#graph").selectAll("*").remove();
            
            if (simulation) {
                simulation.stop();
            }
            
            // Create nodes and links
            const nodes = [];
            for (let i = 0; i < n; i++) {
                nodes.push({id: i, degree: 0});
            }
            
            const links = edges.map(edge => {
                nodes[edge[0]].degree++;
                nodes[edge[1]].degree++;
                return {source: edge[0], target: edge[1]};
            });
            
            const svg = d3.select("#graph");
            const width = 800;
            const height = 500;
            
            svg.attr("width", width).attr("height", height);
            
            // Create force simulation
            simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id).distance(80))
                .force("charge", d3.forceManyBody().strength(-200))
                .force("center", d3.forceCenter(width / 2, height / 2));
            
            // Add links
            const link = svg.append("g")
                .selectAll("line")
                .data(links)
                .enter().append("line")
                .attr("class", "link");
            
            // Add nodes
            const node = svg.append("g")
                .selectAll("circle")
                .data(nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", 15)
                .attr("fill", d => d.degree > 0 ? "#4CAF50" : "#f44336")
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended))
                .on("mouseover", function(event, d) {
                    d3.select(this).attr("r", 18);
                })
                .on("mouseout", function(event, d) {
                    d3.select(this).attr("r", 15);
                });
            
            // Add labels
            const labels = svg.append("g")
                .selectAll("text")
                .data(nodes)
                .enter().append("text")
                .attr("class", "node-label")
                .text(d => d.id);
            
            // Update positions
            simulation.on("tick", () => {
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);
                
                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);
                
                labels
                    .attr("x", d => d.x)
                    .attr("y", d => d.y);
            });
            
            showGraphInfo(nodes, links);
        }
        
        function showGraphInfo(nodes, links) {
            const degrees = nodes.map(n => n.degree);
            const maxDegree = Math.max(...degrees);
            const minDegree = Math.min(...degrees);
            const avgDegree = degrees.reduce((a, b) => a + b, 0) / degrees.length;
            
            const info = `
                <strong>Nodes:</strong> ${nodes.length}<br>
                <strong>Edges:</strong> ${links.length}<br>
                <strong>Max Degree:</strong> ${maxDegree}<br>
                <strong>Min Degree:</strong> ${minDegree}<br>
                <strong>Avg Degree:</strong> ${avgDegree.toFixed(2)}<br>
                <strong>Node Degrees:</strong> ${nodes.map(n => n.id + '(' + n.degree + ')').join(', ')}
            `;
            
            document.getElementById('graph-info').innerHTML = info;
            document.getElementById('info-section').style.display = 'block';
        }
        
        function loadExample(type) {
            let n, edgesStr;
            
            switch(type) {
                case 'star':
                    n = 5;
                    edgesStr = '0 1\n0 2\n0 3\n0 4';
                    break;
                case 'cycle':
                    n = 5;
                    edgesStr = '0 1\n1 2\n2 3\n3 4\n4 0';
                    break;
                case 'tree':
                    n = 7;
                    edgesStr = '0 1\n0 2\n1 3\n1 4\n2 5\n2 6';
                    break;
                case 'complete':
                    n = 4;
                    edgesStr = '0 1\n0 2\n0 3\n1 2\n1 3\n2 3';
                    break;
                case 'path':
                    n = 5;
                    edgesStr = '0 1\n1 2\n2 3\n3 4';
                    break;
                case 'grid':
                    n = 9;
                    edgesStr = '0 1\n1 2\n3 4\n4 5\n6 7\n7 8\n0 3\n1 4\n2 5\n3 6\n4 7\n5 8';
                    break;
            }
            
            document.getElementById('n-input').value = n;
            document.getElementById('edges-input').value = edgesStr;
            visualizeGraph();
        }
        
        function clearAll() {
            document.getElementById('n-input').value = '';
            document.getElementById('edges-input').value = '';
            document.getElementById('info-section').style.display = 'none';
            d3.select("#graph").selectAll("*").remove();
            clearError();
            if (simulation) simulation.stop();
        }
        
        function dragstarted(event, d) {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        }
        
        function dragged(event, d) {
            d.fx = event.x;
            d.fy = event.y;
        }
        
        function dragended(event, d) {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        }
        
        // Load default example on page load
        window.onload = function() {
            visualizeGraph();
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    print("🚀 Starting Graph Visualizer...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped!")