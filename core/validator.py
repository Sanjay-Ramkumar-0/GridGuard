def check_supply_demand(model):
    total_supply = sum(g["capacity"] for g in model.generators)
    total_demand = sum(l["demand"] for l in model.loads)

    if total_supply < total_demand:
        return f"ERROR: Supply ({total_supply}) < Demand ({total_demand})"
    
    return "OK: Supply meets demand"
def check_connectivity(model):
    visited = set()

    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        for neighbor in model.graph.get(node, []):
            dfs(neighbor)

    # Start DFS from all generators
    for g in model.generators:
        dfs(g["id"])

    errors = []

    # Check each load
    for load in model.loads:
        if load["id"] not in visited:
            errors.append(f"ERROR: Load {load['id']} is not connected to any generator")

    return errors
def check_line_capacity(model):
    errors = []

    # Create quick lookup for loads
    load_demand = {l["id"]: l["demand"] for l in model.loads}

    for line in model.lines:
        from_node = line["from"]
        to_node = line["to"]
        capacity = line["capacity"]

        # If line goes directly to a load
        if to_node in load_demand:
            demand = load_demand[to_node]

            if demand > capacity:
                errors.append(
                    f"ERROR: Line ({from_node} → {to_node}) overloaded | Demand = {demand}, Capacity = {capacity}"
                )

    return errors
def check_isolated_nodes(model):
    errors = []

    # Count connections
    connection_count = {}

    # Initialize all nodes
    all_nodes = []

    for g in model.generators:
        all_nodes.append(g["id"])
    for s in model.substations:
        all_nodes.append(s["id"])
    for l in model.loads:
        all_nodes.append(l["id"])

    for node in all_nodes:
        connection_count[node] = 0

    # Count connections from lines
    for line in model.lines:
        connection_count[line["from"]] += 1
        connection_count[line["to"]] += 1

    # Check isolated nodes
    for node, count in connection_count.items():
        if count == 0:
            errors.append(f"WARNING: Node {node} is isolated (no connections)")

    return errors
def check_redundancy(model):
    errors = []

    def dfs_paths(current, target, visited):
        if current == target:
            return 1

        visited.add(current)
        path_count = 0

        for neighbor in model.graph.get(current, []):
            if neighbor not in visited:
                path_count += dfs_paths(neighbor, target, visited.copy())

        return path_count

    for load in model.loads:
        total_paths = 0

        for g in model.generators:
            total_paths += dfs_paths(g["id"], load["id"], set())

        if total_paths < 2:
            errors.append(
                f"WARNING: Load {load['id']} has no redundancy (only {total_paths} path)"
            )

    return errors
def check_bottlenecks(model):
    errors = []

    # Load demand lookup
    load_demand = {l["id"]: l["demand"] for l in model.loads}

    # Initialize flow count for each node
    node_load = {}

    # Initialize all nodes
    for g in model.generators:
        node_load[g["id"]] = 0
    for s in model.substations:
        node_load[s["id"]] = 0
    for l in model.loads:
        node_load[l["id"]] = 0

    # Accumulate load through paths (simplified)
    for line in model.lines:
        to_node = line["to"]

        if to_node in load_demand:
            demand = load_demand[to_node]

            # Add demand to both ends
            node_load[line["from"]] += demand
            node_load[to_node] += demand

    # Detect bottlenecks (threshold-based)
    THRESHOLD = 100  # You can tune this

    for node, load in node_load.items():
        if load > THRESHOLD:
            errors.append(
                f"WARNING: Bottleneck at {node} | Load handled = {load}"
            )

    return errors