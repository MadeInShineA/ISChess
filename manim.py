from manim import *

class TreeLayout(Scene):
    def construct(self):
        self.camera.background_color = GRAY_A

        vertices_by_color = {"WHITE": [1, 4, 5, 6, 7], "BLACK": [2, 3]}
        vertices = [v for group in vertices_by_color.values() for v in group]

        vertex_config = {
            v: {
                "fill_color": color,
                "label": str(v),  # Label text
                "label_color": "WHITE" if color == "BLACK" else "BLACK"
            }
            for color, group in vertices_by_color.items()
            for v in group
        }

        # Create the graph
        graph = Graph(
            vertices,
            [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]}
                for v in vertex_config
            },
            layout="tree",
            layout_config={"root_vertex": 1},
            labels={v: Text(vertex_config[v]["label"], color=vertex_config[v]["label_color"]) for v in vertex_config}
        )

        self.add(graph)
