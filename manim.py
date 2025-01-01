from manim import *
from collections import defaultdict


class TreeLayout(Scene):
    def construct(self):
        self.camera.background_color = GRAY_A

        vertices_by_color = {"WHITE": [(1, "2"), (4, "-4"), (5, "-2"), (6, "4"), (7, "2")], "BLACK": [(2, "-2"), (3, "2")]}
        vertices = [vertice for group in vertices_by_color.values() for vertice, label in group]

        vertex_config = {
            v: {
                "fill_color": color,
                "label": label,  # Label text
                "label_color": "WHITE" if color == "BLACK" else "BLACK"
            }
            for color, group in vertices_by_color.items()
            for v, label in group
        }
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)]

        # Create the graph
        graph = Graph(
            vertices,
            edges,
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]}
                for v in vertex_config
            },
            layout="tree",
            layout_config={"root_vertex": 1},
            labels={v: Text(vertex_config[v]["label"], color=vertex_config[v]["label_color"]) for v in vertex_config}
        )

        dfs_graph = defaultdict(list)

        for source, destination in edges:
            dfs_graph[source].append(destination)
            dfs_graph[destination].append(source)


        visited = {1}
        queue = [1]

        while queue:
            node = queue.pop(0) 
            for neighbor in dfs_graph[node]:
                if neighbor not in visited:
                    self.play(graph.vertices[neighbor].animate.set_color(RED))
                    visited.add(neighbor)
                    queue.append(neighbor)

