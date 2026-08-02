        


class GraphQuery:
    def __init__(self, graph):

        self.graph = graph

    ####################################################################
            # FIND NODES
    ####################################################################

    def find_nodes(

            self,

            entity_type=None,

            domain=None,

            business_area=None,

            category=None,

        ):
            """
            Returns nodes matching supplied filters.

            Parameters
            ----------
            entity_type : str

            domain : str

            business_area : str

            category : str

            Returns
            -------
            list[GraphNode]
            """

            results = []

            for node in self.graph.get_nodes():

                if entity_type:

                    if node.entity_type.lower() != entity_type.lower():

                        continue

                if domain:

                    if node.domain.lower() != domain.lower():

                        continue

                if business_area:

                    if node.business_area.lower() != business_area.lower():

                        continue

                if category:

                    if node.category.lower() != category.lower():

                        continue

                results.append(node)

            return results
            ####################################################################
        # FIND SINGLE NODE
        ####################################################################

    def find_node(

            self,

            node_id=None,

            canonical=None,

        ):
            """
            Finds a single node.

            Parameters
            ----------
            node_id : str

            canonical : str

            Returns
            -------
            GraphNode | None
            """

            # ----------------------------------------------------------
            # Search by Node ID
            # ----------------------------------------------------------

            if node_id:

                return self.graph.get_node(node_id)

            # ----------------------------------------------------------
            # Search by Canonical Name
            # ----------------------------------------------------------

            if canonical:

                canonical = canonical.lower().strip()

                for node in self.graph.get_nodes():

                    if node.canonical.lower() == canonical:

                        return node

            return None
            ####################################################################
        # FIND EDGES
        ####################################################################

    def find_edges(

            self,

            relation=None,

            source_id=None,

            target_id=None,

        ):
            """
            Returns graph edges matching filters.

            Parameters
            ----------
            relation : str

            source_id : str

            target_id : str

            Returns
            -------
            list[GraphEdge]
            """

            results = []

            for edge in self.graph.get_edges():

                # ------------------------------------------------------
                # Relation
                # ------------------------------------------------------

                if relation:

                    if edge.relation.lower() != relation.lower():

                        continue

                # ------------------------------------------------------
                # Source
                # ------------------------------------------------------

                if source_id:

                    if edge.source_id != source_id:

                        continue

                # ------------------------------------------------------
                # Target
                # ------------------------------------------------------

                if target_id:

                    if edge.target_id != target_id:

                        continue

                results.append(edge)

            return results
        ####################################################################
        # GET NEIGHBOR NODES
        ####################################################################

    def neighbors(

            self,

            node_id,

            relation=None,

            direction="both",

        ):
            """
            Returns neighboring nodes connected to a node.

            Parameters
            ----------
            node_id : str

            relation : str | None

            direction :
                "out"
                "in"
                "both"

            Returns
            -------
            list[GraphNode]
            """

            neighbors = []

            seen = set()

            # ----------------------------------------------------------
            # Outgoing Relations
            # ----------------------------------------------------------

            if direction in ("out", "both"):

                outgoing = self.find_edges(

                    relation=relation,

                    source_id=node_id,

                )

                for edge in outgoing:

                    node = self.graph.get_node(

                        edge.target_id

                    )

                    if node and node.node_id not in seen:

                        neighbors.append(node)

                        seen.add(node.node_id)

            # ----------------------------------------------------------
            # Incoming Relations
            # ----------------------------------------------------------

            if direction in ("in", "both"):

                incoming = self.find_edges(

                    relation=relation,

                    target_id=node_id,

                )

                for edge in incoming:

                    node = self.graph.get_node(

                        edge.source_id

                    )

                    if node and node.node_id not in seen:

                        neighbors.append(node)

                        seen.add(node.node_id)

            return neighbors
        ####################################################################
        # FIND BY RELATION
        ####################################################################

    def find_by_relation(

            self,

            relation,

            source_id=None,

            target_id=None,

        ):
            """
            Finds relationships and returns
            source/target node pairs.

            Parameters
            ----------
            relation : str

            source_id : str | None

            target_id : str | None

            Returns
            -------
            list[dict]
            """

            results = []

            edges = self.find_edges(

                relation=relation,

                source_id=source_id,

                target_id=target_id,

            )

            for edge in edges:

                source = self.graph.get_node(

                    edge.source_id

                )

                target = self.graph.get_node(

                    edge.target_id

                )

                results.append(

                    {

                        "relation": edge.relation,

                        "source": source,

                        "target": target,

                        "confidence": edge.confidence,

                        "reasoning": edge.reasoning,

                    }

                )

            return results

        ####################################################################
        # SHORTEST PATH (BFS)
        ####################################################################

    def shortest_path(

            self,

            start_node_id,

            end_node_id,

        ):
            """
            Finds the shortest path between two nodes
            using Breadth-First Search.

            Returns
            -------
            list[GraphNode]
            """

            if start_node_id == end_node_id:

                node = self.graph.get_node(start_node_id)

                return [node] if node else []

            visited = set()

            queue = [

                (

                    start_node_id,

                    [start_node_id],

                )

            ]

            while queue:

                current_node, path = queue.pop(0)

                if current_node in visited:

                    continue

                visited.add(current_node)

                neighbors = self.neighbors(

                    current_node,

                    direction="out",

                )

                for neighbor in neighbors:

                    if neighbor.node_id == end_node_id:

                        final_path = path + [

                            neighbor.node_id

                        ]

                        return [

                            self.graph.get_node(node_id)

                            for node_id in final_path

                        ]

                    if neighbor.node_id not in visited:

                        queue.append(

                            (

                                neighbor.node_id,

                                path + [

                                    neighbor.node_id

                                ],

                            )

                        )

            return []