class GridModel:
    def __init__(self, data):
        self.generators = data["generators"]
        self.substations = data["substations"]
        self.loads = data["loads"]
        self.lines = data["lines"]

        self.graph = {}
        self.build_graph()

    def build_graph(self):
        # initialize nodes
        for g in self.generators:
            self.graph[g["id"]] = []

        for s in self.substations:
            self.graph[s["id"]] = []

        for l in self.loads:
            self.graph[l["id"]] = []

        # add edges
        for line in self.lines:
            self.graph[line["from"]].append(line["to"])
