"""
Knowledge Graph Visualizer

Creates a readable graph representation.

Later this can export to:

NetworkX
Neo4j
GraphViz
Mermaid
D3.js
"""

from pprint import pprint


class GraphVisualizer:

    def __init__(self, graph):

        self.graph = graph

    # ---------------------------------------------------------

    def print_nodes(self):

        print("\n========================")
        print("GRAPH NODES")
        print("========================\n")

        for node in self.graph.nodes:

            pprint(node)

    # ---------------------------------------------------------

    def print_edges(self):

        print("\n========================")
        print("GRAPH EDGES")
        print("========================\n")

        for edge in self.graph.edges:

            pprint(edge)

    # ---------------------------------------------------------

    def print_summary(self):

        print("\n========================")
        print("GRAPH SUMMARY")
        print("========================")

        print(f"Nodes : {len(self.graph.nodes)}")
        print(f"Edges : {len(self.graph.edges)}")

    # ---------------------------------------------------------

    def adjacency_list(self):

        print("\n========================")
        print("GRAPH CONNECTIONS")
        print("========================\n")

        for edge in self.graph.edges:

            print(
                f"{edge.source_node}"
                f" --{edge.relationship}--> "
                f"{edge.target_node}"
            )

    # ---------------------------------------------------------

    def mermaid(self):

        """
        Generates Mermaid syntax.

        Can be pasted into

        https://mermaid.live
        """

        lines = ["graph TD"]

        for edge in self.graph.edges:

            lines.append(
                f'{edge.source_node}["{edge.source_node}"]'
                f' -->|{edge.relationship}| '
                f'{edge.target_node}["{edge.target_node}"]'
            )

        return "\n".join(lines)