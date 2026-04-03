def generate_suggestions(model):
    suggestions = []

    # ===============================
    # 1. Supply-Demand Suggestions
    # ===============================
    total_supply = sum(g["capacity"] for g in model.generators)
    total_demand = sum(l["demand"] for l in model.loads)

    if total_supply < total_demand:
        deficit = total_demand - total_supply
        suggestions.append(
            f"Power deficit detected: {deficit} MW\n"
            f"  → Option 1: Add new generator ≥ {deficit} MW\n"
            f"  → Option 2: Reduce load by {deficit} MW\n"
            f"  → Option 3: Redistribute load across additional sources"
        )

    # ===============================
    # 2. Connectivity Suggestions
    # ===============================
    connected_nodes = set()

    def dfs(node):
        if node in connected_nodes:
            return
        connected_nodes.add(node)
        for neighbor in model.graph.get(node, []):
            dfs(neighbor)

    for g in model.generators:
        dfs(g["id"])

    for load in model.loads:
        if load["id"] not in connected_nodes:
            suggestions.append(
                f"Load {load['id']} is disconnected\n"
                f"  → Option 1: Connect to nearest substation\n"
                f"  → Option 2: Create direct connection from generator\n"
                f"  → Option 3: Add intermediate substation for routing"
            )

    # ===============================
    # 3. Line Capacity Suggestions
    # ===============================
    load_demand = {l["id"]: l["demand"] for l in model.loads}

    for line in model.lines:
        from_node = line["from"]
        to_node = line["to"]
        capacity = line["capacity"]

        if to_node in load_demand:
            demand = load_demand[to_node]

            if demand > capacity:
                suggestions.append(
                    f"Line ({from_node} → {to_node}) is overloaded\n"
                    f"  → Required: {demand} MW | Capacity: {capacity} MW\n"
                    f"  → Option 1: Upgrade line capacity to ≥ {demand} MW\n"
                    f"  → Option 2: Add parallel transmission line\n"
                    f"  → Option 3: Redistribute load via alternate path"
                )

    return suggestions