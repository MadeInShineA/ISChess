from manim import *
import networkx as nx

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
        edges = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)][::-1]

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


        self.add(graph)

class DFS(Scene):
    def construct(self):

        self.camera.background_color = GRAY_A

        graph_dict = {
            "2_depth_0": ["2_depth_1", "-2_depth_1"],  # Use list instead of set
            "2_depth_1": ["4_depth_2", "2_depth_2"],
            "-2_depth_1": ["-4_depth_2", "-2_depth_2"],
            "4_depth_2": [],
            "2_depth_2": [],
            "-2_depth_2": [],
            "-4_depth_2": []
        }

        visited = []
        def dfs(vertex, parent):
            visited.append((vertex, parent))
            for neighbor in graph_dict[vertex]:
                if neighbor not in visited:
                    dfs(neighbor, vertex)

        dfs("2_depth_0", None)

        vertices = [node for node, parent in visited]
        edges = [(parent, node) for node, parent in visited if parent is not None]
        
        even_depth_nodes_colors = {node: "WHITE" for node in graph_dict.keys() if int(node[-1]) % 2 == 0}
        odd_depth_nodes_colors = {node: "BLACK" for node in graph_dict.keys() if int(node[-1]) % 2 != 0}

        vertices_colors = even_depth_nodes_colors | odd_depth_nodes_colors
        vertices_labels = {node: node[0] if node[0] != "-" else node[0:2] for node in graph_dict.keys()}

        vertex_config = {
            vertex: {
                "fill_color": vertices_colors[vertex],
                "label": vertices_labels[vertex],
                "label_color": "WHITE" if vertices_colors[vertex] == "BLACK" else "BLACK"
            } for vertex in vertices
        }

        manim_graph = DiGraph(
            vertices,
            edges,
            layout="tree",
            root_vertex="2_depth_0",
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]}
                for v in vertex_config
            },
            labels={v: Text(vertex_config[v]["label"], color=vertex_config[v]["label_color"]) for v in vertex_config}
        )

        self.play(Create(manim_graph))
        self.wait()

class MinMaxTree(Scene):
    def construct(self):

        self.camera.background_color = GRAY_A

        graph_dict = {
            "2_depth_0": ["2_depth_1", "-2_depth_1"],  # Use list instead of set
            "2_depth_1": ["4_depth_2", "2_depth_2"],
            "-2_depth_1": ["-4_depth_2", "-2_depth_2"],
            "4_depth_2": [],
            "2_depth_2": [],
            "-2_depth_2": [],
            "-4_depth_2": []
        }

        visited = []
        def dfs(vertex, parent):
            visited.append((vertex, parent))
            for neighbor in graph_dict[vertex]:
                if (neighbor, vertex) not in visited:
                    dfs(neighbor, vertex)

        dfs("2_depth_0", None)

        vertices = [node for node, parent in visited]
        edges = [(parent, node) for node, parent in visited if parent is not None]
        
        even_depth_nodes_colors = {node: "WHITE" for node in graph_dict.keys() if int(node[-1]) % 2 == 0}
        odd_depth_nodes_colors = {node: "BLACK" for node in graph_dict.keys() if int(node[-1]) % 2 != 0}

        vertices_colors = even_depth_nodes_colors | odd_depth_nodes_colors
        vertices_labels = {node: node[0] if node[0] != "-" else node[0:2] for node in graph_dict.keys()}

        vertex_config = {
            vertex: {
                "fill_color": vertices_colors[vertex],
                "label": vertices_labels[vertex],
                "label_color": "WHITE" if vertices_colors[vertex] == "BLACK" else "BLACK"
            } for vertex in vertices
        }

        graphs = []

        for i in range(1, len(visited)):
            vertices = [node for node, parent in visited[:i]]
            edges = [(parent, node) for node, parent in visited[:i] if parent is not None]
            
            print("====")
            print(vertices)
            print(edges)

            vertex_config = {
                vertex: {
                    "fill_color": vertices_colors[vertex],
                    "label": vertices_labels[vertex],
                    "label_color": "WHITE" if vertices_colors[vertex] == "BLACK" else "BLACK"
                } for vertex in vertices
            }

            graph = DiGraph(
                vertices,
                edges,
                layout="tree",
                root_vertex="2_depth_0",
                vertex_config={
                    v: {"fill_color": vertex_config[v]["fill_color"]}
                    for v in vertex_config
                },
                labels={v: Text(vertex_config[v]["label"], color=vertex_config[v]["label_color"]) for v in vertex_config}
            )

            graphs.append(graph)

        self.play(Create(graphs[0]))
        for i in range(1, len(graphs)):
            print(graphs[i])

            self.play(Transform(graphs[i - 1], graphs[i]))
            self.wait()
        self.wait()
