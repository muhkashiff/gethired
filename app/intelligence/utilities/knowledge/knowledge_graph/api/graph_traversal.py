"""
Enterprise Graph Traversal API

Provides graph exploration algorithms.

Supports:

- Breadth First Search
- Depth First Search
- Upstream traversal
- Downstream traversal
- Relation based traversal
- Depth limited exploration

Enterprise Version
"""


from collections import deque


class GraphTraversal:

    def __init__(self, graph):

        self.graph = graph


    # =====================================================
    # DOWNSTREAM TRAVERSAL
    # =====================================================

    def downstream(

        self,

        node_id,

        depth=1,

    ):

        """
        Follow outgoing relationships.

        Example:

        Action
            |
            affects
            ↓
        Metric
            |
            measured_by
            ↓
        Measurement
        """

        visited = set()

        results = []

        self._dfs_downstream(

            node_id,

            depth,

            visited,

            results,

        )

        return results



    def _dfs_downstream(

        self,

        node_id,

        depth,

        visited,

        results,

    ):

        if depth == 0:

            return


        if node_id in visited:

            return


        visited.add(node_id)


        for edge in self.graph.edges:


            if edge.source_id == node_id:


                target = self.graph.get_node(

                    edge.target_id

                )


                if target:


                    results.append(target)


                    self._dfs_downstream(

                        target.node_id,

                        depth - 1,

                        visited,

                        results,

                    )



    # =====================================================
    # UPSTREAM TRAVERSAL
    # =====================================================

    def upstream(

        self,

        node_id,

        depth=1,

    ):

        """
        Reverse traversal.

        Example:

        Measurement

             ↑

        Metric

             ↑

        Action
        """

        visited=set()

        results=[]


        self._dfs_upstream(

            node_id,

            depth,

            visited,

            results,

        )


        return results



    def _dfs_upstream(

        self,

        node_id,

        depth,

        visited,

        results,

    ):


        if depth == 0:

            return


        if node_id in visited:

            return


        visited.add(node_id)


        for edge in self.graph.edges:


            if edge.target_id == node_id:


                source = self.graph.get_node(

                    edge.source_id

                )


                if source:


                    results.append(source)


                    self._dfs_upstream(

                        source.node_id,

                        depth - 1,

                        visited,

                        results,

                    )



    # =====================================================
    # BREADTH FIRST SEARCH
    # =====================================================

    def bfs(

        self,

        start_node,

        max_depth=5,

    ):

        """
        Breadth First Search.

        Useful for AI reasoning.
        """

        visited=set()

        queue=deque()


        queue.append(

            (

                start_node,

                0

            )

        )


        results=[]


        while queue:


            node_id, depth = queue.popleft()


            if node_id in visited:

                continue


            visited.add(node_id)


            node=self.graph.get_node(

                node_id

            )


            if node:

                results.append(node)


            if depth >= max_depth:

                continue



            for edge in self.graph.edges:


                if edge.source_id == node_id:


                    queue.append(

                        (

                            edge.target_id,

                            depth + 1

                        )

                    )


                elif edge.target_id == node_id:


                    queue.append(

                        (

                            edge.source_id,

                            depth + 1

                        )

                    )


        return results



    # =====================================================
    # RELATION TRAVERSAL
    # =====================================================

    def follow_relation(

        self,

        node_id,

        relation,

    ):

        """
        Follow only a specific relationship.

        Example:

        implemented
             |
             complies_with
             ↓
        FSSC22000
        """

        relation = relation.lower()


        results=[]


        for edge in self.graph.edges:


            if (

                edge.source_id == node_id

                and

                edge.relation.lower()

                == relation

            ):


                node=self.graph.get_node(

                    edge.target_id

                )


                if node:

                    results.append(node)


        return results



    # =====================================================
    # PATH FINDING
    # =====================================================

    def find_path(

        self,

        start,

        target,

    ):

        """
        Finds relationship path.

        Example:

        Action
          |
          |
        Achievement
          |
          |
        KPI

        """

        queue=deque()


        queue.append(

            [

                start

            ]

        )


        visited=set()



        while queue:


            path=queue.popleft()


            current=path[-1]


            if current == target:

                return path



            if current in visited:

                continue


            visited.add(current)



            for edge in self.graph.edges:


                if edge.source_id == current:


                    queue.append(

                        path +

                        [

                            edge.target_id

                        ]

                    )


        return []
