from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from core.model import GridModel
from core.validator import (
    check_supply_demand,
    check_connectivity,
    check_line_capacity,
    check_isolated_nodes,
    check_redundancy
)
from core.suggestion import generate_suggestions

import json

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>GridGuard</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600&display=swap');
            
            body {
                font-family: 'Inter', system-ui, sans-serif;
                background: #0a0a0a;
                color: #d1d5db;
                margin: 0;
                padding: 0;
                min-height: 100vh;
                background-image: 
                    radial-gradient(circle at 50% 30%, rgba(45, 212, 191, 0.08) 0%, transparent 50%);
            }
            
            .container {
                max-width: 960px;
                margin: 60px auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 50px;
            }
            
            .header h1 {
                font-family: 'Space Grotesk', sans-serif;
                font-size: 3.2rem;
                font-weight: 600;
                color: #e5e7eb;
                margin: 0;
                letter-spacing: -0.02em;
            }
            
            .header p {
                color: #9ca3af;
                font-size: 1.05rem;
                margin-top: 8px;
                letter-spacing: 0.5px;
            }
            
            .main-card {
                background: #111111;
                border: 1px solid #27272a;
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
            }
            
            h2 {
                color: #e5e7eb;
                font-size: 1.35rem;
                margin-top: 0;
                margin-bottom: 8px;
                font-weight: 600;
            }
            
            .description {
                color: #9ca3af;
                margin-bottom: 24px;
                font-size: 0.98rem;
            }
            
            textarea {
                width: 100%;
                height: 420px;
                background: #0a0a0a;
                color: #d1d5db;
                border: 1px solid #3f3f46;
                border-radius: 8px;
                padding: 20px;
                font-family: 'Space Grotesk', monospace;
                font-size: 15px;
                line-height: 1.5;
                resize: vertical;
                margin-bottom: 24px;
            }
            
            textarea:focus {
                outline: none;
                border-color: #14b8a6;
                box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.15);
            }
            
            button {
                background: linear-gradient(to right, #14b8a6, #0ea5e9);
                color: white;
                border: none;
                padding: 16px 40px;
                font-size: 1.05rem;
                font-weight: 600;
                border-radius: 8px;
                cursor: pointer;
                transition: all 0.3s ease;
                width: 100%;
            }
            
            button:hover {
                background: linear-gradient(to right, #0ea5e9, #14b8a6);
                transform: translateY(-1px);
            }
            
            .footer {
                text-align: center;
                margin-top: 50px;
                color: #52525b;
                font-size: 0.9rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>GridGuard</h1>
                <p>Intelligent Power Grid Analysis & Validation Tool</p>
            </div>
            
            <div class="main-card">
                <h2>Enter Grid Configuration</h2>
                <p class="description">Paste your grid data in JSON format below:</p>
                
                <form method="post" action="/analyze">
                    <textarea name="data" spellcheck="false">{
  "generators": [{"id": "G1", "capacity": 100}],
  "substations": [{"id": "S1"}],
  "loads": [{"id": "L1", "demand": 60}],
  "lines": [
    {"from": "G1", "to": "S1", "capacity": 80},
    {"from": "S1", "to": "L1", "capacity": 40}
  ]
}</textarea>
                    
                    <button type="submit">Analyze Grid</button>
                </form>
            </div>
            
            <div class="footer">
                GridGuard • Power System Validation Tool
            </div>
        </div>
    </body>
    </html>
    """


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request):
    form = await request.form()
    data_str = form["data"]

    try:
        data = json.loads(data_str)
        model = GridModel(data)

        errors = []
        warnings = []

        result = check_supply_demand(model)
        if "ERROR" in result:
            errors.append(result)

        errors.extend(check_connectivity(model))
        errors.extend(check_line_capacity(model))
        warnings.extend(check_isolated_nodes(model))
        warnings.extend(check_redundancy(model))

        suggestions = generate_suggestions(model)

        # ================= ERROR TRACKING FOR GRAPH HIGHLIGHTING =================
        error_nodes = set()
        error_edges = set()

        # Connectivity errors → mark loads
        for err in errors:
            if "Load" in err:
                parts = err.split()
                if len(parts) > 2:
                    error_nodes.add(parts[2])

        # Line overload → mark edges
        for err in errors:
            if "Line (" in err:
                # Extract from "Line (S1 → L1)"
                start = err.find("(") + 1
                end = err.find(")")
                if start != -1 and end != -1:
                    src, tgt = err[start:end].split(" → ")
                    error_edges.add((src, tgt))

        # ================= GRAPH DATA =================
        nodes = []
        edges = []

        # Nodes with status (exactly as requested + capacity/demand kept for info popup)
        for g in model.generators:
            nodes.append({
                "data": {
                    "id": g["id"],
                    "type": "generator",
                    "capacity": g["capacity"],
                    "status": "error" if g["id"] in error_nodes else "normal"
                }
            })

        for s in model.substations:
            nodes.append({
                "data": {
                    "id": s["id"],
                    "type": "substation",
                    "status": "error" if s["id"] in error_nodes else "normal"
                }
            })

        for l in model.loads:
            nodes.append({
                "data": {
                    "id": l["id"],
                    "type": "load",
                    "demand": l["demand"],
                    "status": "error" if l["id"] in error_nodes else "normal"
                }
            })

        # Edges with status
        for line in model.lines:
            status = "error" if (line["from"], line["to"]) in error_edges else "normal"
            edges.append({
                "data": {
                    "source": line["from"],
                    "target": line["to"],
                    "capacity": line["capacity"],
                    "status": status
                }
            })

        graph_data = {"nodes": nodes, "edges": edges}

        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Analysis Result — GridGuard</title>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Space+Grotesk:wght@500;600&display=swap');
                
                body {{
                    font-family: 'Inter', system-ui, sans-serif;
                    background: #0a0a0a;
                    color: #d1d5db;
                    margin: 0;
                    padding: 40px 20px;
                    min-height: 100vh;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                }}
                .main-card {{
                    background: #111111;
                    border: 1px solid #27272a;
                    border-radius: 12px;
                    padding: 40px;
                    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
                }}
                h2 {{
                    color: #e5e7eb;
                    border-bottom: 1px solid #27272a;
                    padding-bottom: 16px;
                    margin-top: 0;
                    font-size: 1.45rem;
                }}
                h3 {{
                    margin-top: 32px;
                    margin-bottom: 12px;
                    color: #a1a1aa;
                    font-weight: 500;
                    font-size: 1.1rem;
                }}
                pre {{
                    background: #0a0a0a;
                    border: 1px solid #27272a;
                    padding: 20px;
                    border-radius: 8px;
                    overflow-x: auto;
                    white-space: pre-wrap;
                    font-size: 14.5px;
                    line-height: 1.55;
                    color: #d1d5db;
                }}
                #graph {{
                    width: 100%;
                    height: 520px;
                    background: #0a0a0a;
                    border: 1px solid #27272a;
                    border-radius: 12px;
                    margin-top: 30px;
                }}
                .back-btn {{
                    display: inline-block;
                    margin-top: 40px;
                    padding: 14px 32px;
                    background: #27272a;
                    color: #d1d5db;
                    text-decoration: none;
                    border-radius: 8px;
                    font-weight: 500;
                    border: 1px solid #3f3f46;
                    transition: all 0.3s;
                }}
                .back-btn:hover {{
                    background: #3f3f46;
                    border-color: #52525b;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="main-card">
                    <h2>Grid Analysis Result</h2>
                    
                    <h3>Errors</h3>
                    <pre>{chr(10).join(errors) if errors else "No errors detected."}</pre>

                    <h3>Warnings</h3>
                    <pre>{chr(10).join(warnings) if warnings else "No warnings detected."}</pre>

                    <h3>Suggestions</h3>
                    <pre>{chr(10).join(suggestions) if suggestions else "No suggestions generated."}</pre>

                    <h3>Network Topology</h3>
                    <div id="graph"></div>

                    <a href="/" class="back-btn">← Back to Configuration</a>
                </div>
            </div>

            <script src="https://unpkg.com/cytoscape@3.26.0/dist/cytoscape.min.js"></script>
            <script>
                const graphData = {json.dumps(graph_data)};

                const generatorIds = graphData.nodes
                    .filter(n => n.data.type === "generator")
                    .map(n => n.data.id);

                const cy = cytoscape({{
                    container: document.getElementById('graph'),

                    elements: [
                        ...graphData.nodes,
                        ...graphData.edges
                    ],

                    style: [
                        {{
                            selector: 'node[type="generator"]',
                            style: {{
                                'background-color': '#14b8a6',
                                'label': 'data(id)',
                                'color': '#fff',
                                'text-valign': 'center',
                                'text-halign': 'center',
                                'font-size': '14px',
                                'font-weight': '700',
                                'width': 58,
                                'height': 58,
                                'border-width': 3,
                                'border-color': '#0f766e'
                            }}
                        }},
                        {{
                            selector: 'node[type="substation"]',
                            style: {{
                                'background-color': '#0ea5e9',
                                'label': 'data(id)',
                                'color': '#fff',
                                'text-valign': 'center',
                                'text-halign': 'center',
                                'font-size': '13px',
                                'font-weight': '600',
                                'width': 48,
                                'height': 48
                            }}
                        }},
                        {{
                            selector: 'node[type="load"]',
                            style: {{
                                'background-color': '#f59e0b',
                                'label': 'data(id)',
                                'color': '#fff',
                                'text-valign': 'center',
                                'text-halign': 'center',
                                'font-size': '13px',
                                'font-weight': '600',
                                'width': 48,
                                'height': 48
                            }}
                        }},
                        {{
                            selector: 'edge',
                            style: {{
                                'width': 3,
                                'line-color': '#64748b',
                                'target-arrow-shape': 'triangle',
                                'target-arrow-color': '#64748b',
                                'curve-style': 'bezier',
                                'label': 'data(capacity)',
                                'font-size': '11px',
                                'font-weight': '500',
                                'color': '#cbd5e1',
                                'text-margin-y': -14,
                                'text-background-color': '#0a0a0a',
                                'text-background-opacity': 0.9,
                                'text-background-padding': '3px'
                            }}
                        }},
                        // 🔴 Muted error highlighting (subtle, professional, not vivid)
                        {{
                            selector: 'node[status="error"]',
                            style: {{
                                'background-color': '#9f1239',
                                'border-width': 3,
                                'border-color': '#e11d48'
                            }}
                        }},
                        {{
                            selector: 'edge[status="error"]',
                            style: {{
                                'line-color': '#9f1239',
                                'target-arrow-color': '#9f1239',
                                'width': 4
                            }}
                        }}
                    ],

                    layout: {{
                        name: 'breadthfirst',
                        directed: true,
                        roots: generatorIds.length > 0 ? generatorIds : undefined,
                        padding: 60,
                        spacingFactor: 1.4,
                        animate: true,
                        animationDuration: 800,
                        nodeDimensionsIncludeLabels: true
                    }}
                }});

                cy.on('layoutstop', () => {{
                    cy.fit(undefined, 40);
                    cy.zoom(1.05);
                }});

                cy.on('tap', 'node', function(evt){{
                    const node = evt.target.data();
                    let info = `Node: ${{node.id}}\\nType: ${{node.type}}`;
                    if (node.capacity !== undefined) info += `\\nCapacity: ${{node.capacity}} MW`;
                    if (node.demand !== undefined) info += `\\nDemand: ${{node.demand}} MW`;
                    alert(info);
                }});

                cy.on('tap', 'edge', function(evt){{
                    const edge = evt.target.data();
                    alert(`Connection: ${{edge.source}} → ${{edge.target}}\\nCapacity: ${{edge.capacity}} MW`);
                }});
            </script>
        </body>
        </html>
        """

    except Exception as e:
        return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Error — GridGuard</title>
            <style>
                body {{ background:#0a0a0a; color:#d1d5db; font-family:Inter,sans-serif; padding:80px 20px; text-align:center; }}
                h2 {{ color:#ef4444; }}
                a {{ color:#14b8a6; text-decoration:none; }}
            </style>
        </head>
        <body>
            <h2>Error Parsing Input</h2>
            <p>{str(e)}</p>
            <br>
            <a href="/">← Back to GridGuard</a>
        </body>
        </html>
        """