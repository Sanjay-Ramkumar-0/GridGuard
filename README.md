# ⚡ GridGuard

**GridGuard** is a next-generation power infrastructure validation and optimization platform that detects design-level failures in electrical grid architectures **before deployment**.

It empowers engineers, planners, utility companies, and researchers to identify critical issues such as overloads, disconnections, supply-demand imbalances, and lack of redundancy — then delivers **actionable, intelligent recommendations** with stunning interactive visualizations.

---

## 🎯 The Problem

Modern power grids are becoming increasingly complex due to renewable integration, urbanization, and electrification. Yet most failures originate from **design-phase inefficiencies**:

- Supply-demand imbalance  
- Overloaded transmission lines  
- Insufficient redundancy  
- Disconnected or orphaned loads  
- Hidden bottlenecks  

These issues are usually discovered **only after deployment**, resulting in:
- Massive cost overruns  
- Reduced system reliability  
- Blackouts and safety risks  
- Delayed project timelines  

---

## 💡 The Solution

**GridGuard** shifts validation from post-deployment firefighting to **early-stage intelligent design**.

It models the entire power grid as a directed graph, performs comprehensive rule-based and capacity-aware analysis, and instantly surfaces problems with clear, prioritized fixes.

**Result**: Safer, more reliable, and cost-effective grid designs — validated before a single wire is laid.

---

## 🚀 Key Features

### 🔍 Validation Engine
- Real-time supply vs demand balancing  
- Full connectivity & reachability validation  
- Line capacity (overload) detection  
- Redundancy & N-1 contingency checks  
- Bottleneck & critical path identification  

### 💡 Intelligent Suggestions
- Automatic capacity upgrade recommendations  
- Network restructuring proposals  
- Load redistribution strategies  
- Prioritized fix list with estimated impact  

### 📊 Interactive Visualization
- Beautiful graph-based grid representation  
- Color-coded error highlighting (🔴 overloads, ⚠️ warnings, 🟢 healthy)  
- Clickable nodes & edges with detailed inspection  
- Real-time analysis feedback  
- Before/After comparison views  

---

## 🧠 How It Works

GridGuard treats the power grid as a **directed graph**:

- **Nodes** → Generators, Substations, Loads  
- **Edges** → Transmission lines (with capacity and flow data)  

It applies a multi-layered validation pipeline:
1. Structural validation (connectivity, reachability)  
2. Capacity & flow analysis  
3. Reliability & redundancy scoring  
4. Intelligent recommendation engine  

All processing happens instantly in the browser/backend with zero external dependencies.

---

## 🎥 Demo Workflow

The live demo showcases a complete validation cycle:

### ❌ **Broken Grid** (`broken.json`)
- Multiple critical failures  
- Severe overloads & disconnections  
- Supply deficit  

### 🟡 **Fixed Grid** (`fixed.json`)
- Connectivity restored  
- Overloads significantly reduced  

### ✅ **Optimized Grid** (`optimized.json`)
- Perfectly balanced system  
- Full redundancy achieved  
- Optimal performance & stability  

Try all three JSON files in the interactive demo to see GridGuard in action.

---

## 📂 Project Structure

```
GridGuard/
├── app.py              # FastAPI backend + API endpoints
├── core/               # Validation engine & graph logic
├── utils/              # Helper functions & data models
├── demo/               # Sample grid JSON files
│   ├── broken.json
│   ├── fixed.json
│   └── optimized.json
├── static/             # Frontend assets (HTML + JS + CSS)
├── templates/          # Jinja/HTML templates
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/gridguard.git
cd gridguard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
uvicorn app:app --reload
```

**Open your browser** → [http://127.0.0.1:8000](http://127.0.0.1:8000)

Upload any grid JSON or use the built-in demo files to start validating instantly.

---

## 🌍 Use Cases

- Smart city & renewable energy infrastructure planning  
- Utility-scale power grid design validation  
- Academic research & power systems education  
- Government & regulatory compliance testing  
- Microgrid and campus energy system optimization  

---

## 🔥 Why GridGuard Stands Out

| Feature                      | Traditional Tools      | GridGuard                  |
|-----------------------------|------------------------|----------------------------|
| Validation Phase            | Post-deployment        | **Design phase**           |
| Output                      | Detection only         | **Detection + Fixes**      |
| Visualization               | Static diagrams        | **Interactive + Real-time**|
| Speed                       | Slow simulations       | **Instant analysis**       |
| Accessibility               | Expert-only            | Engineer & planner friendly|

---

## 🚀 Future Roadmap

- AI-powered optimization engine  
- Real-time integration with SCADA/EMS systems  
- Cost-benefit & ROI analysis  
- Multi-scenario simulation & Monte Carlo analysis  
- Cloud SaaS version with collaboration features  
- Exportable professional reports (PDF/Excel)  

---

## 👨‍💻 Author

**Sanjay Ramkumar**  
 

📧 ss.ramsanjay@gmail.com  
🔗 [LinkedIn](www.linkedin.com/in/sanjay-ramkumar-5b954031b) | [GitHub]([https://github.com/yourusername](https://github.com/Sanjay-Ramkumar-0))

---

## 📌 Vision

To make intelligent, failure-proof infrastructure design the **standard** — not the exception.  

GridGuard turns complex grid validation into a simple, visual, and actionable process — helping build the resilient power systems of tomorrow.
