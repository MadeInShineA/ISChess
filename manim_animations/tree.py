from manim import *


class Tree(Scene):
    def construct(self):
        self.camera.background_color = GRAY_A

        vertices_by_color = {
            "WHITE": [(1, "2"), (4, "-4"), (5, "-2"), (6, "4"), (7, "2")],
            "BLACK": [(2, "-2"), (3, "2")],
        }
        vertices = [
            vertice for group in vertices_by_color.values() for vertice, label in group
        ]

        vertex_config = {
            v: {
                "fill_color": color,
                "label": label,  # Label text
                "label_color": "WHITE" if color == "BLACK" else "BLACK",
            }
            for color, group in vertices_by_color.items()
            for v, label in group
        }
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)][::-1]

        # Create the graph
        graph = Graph(
            vertices,
            edges,
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]} for v in vertex_config
            },
            layout="tree",
            layout_config={"root_vertex": 1},
            labels={
                v: Text(
                    vertex_config[v]["label"], color=vertex_config[v]["label_color"]
                )
                for v in vertex_config
            },
        )

        self.add(graph)
