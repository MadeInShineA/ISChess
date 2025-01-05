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

class MinMax(Scene):
    def construct(self):

        self.camera.background_color = GRAY_A

        graph_dict = {
            "2_depth_0": ["2_depth_1", "-4_depth_1"],  # Use list instead of set
            "2_depth_1": ["4_depth_2", "2_depth_2"],
            "-4_depth_1": ["-4_depth_2", "-2_depth_2"],
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
        vertices_values = {node: int(node.split("_")[0]) for node in graph_dict.keys()}

        vertex_config = {
            vertex: {
                "fill_color": vertices_colors[vertex],
                "value": vertices_values[vertex],
                "label_color": "WHITE" if vertices_colors[vertex] == "BLACK" else "BLACK"
            } for vertex in vertices
        }

        labels = {v: Text("?", color=vertex_config[v]["label_color"]) for v in vertex_config}

        manim_graph = DiGraph(
            vertices,
            edges=edges[::-1],
            layout="tree",
            root_vertex="2_depth_0",
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]}
                for v in vertex_config
            },
            labels=labels
        )

        def all_descendants_added(vertice, added_vertices, graph_dict):
            children = graph_dict[vertice]
            if not children:
                return True
            return all(child in added_vertices and all_descendants_added(child, added_vertices, graph_dict) for child in children)

        def change_label_to_value(vertice):
            old_label = labels[vertice]

            new_label = Text(str(vertex_config[vertice]["value"]), color=vertex_config[vertice]["label_color"])
            new_label.move_to(manim_graph[vertice].get_center())
            labels[vertice] = new_label
            self.play(Transform(old_label, new_label))


        added_vertices = set()

        for vertice, parent in visited:
            if parent:
                self.play(Create(manim_graph.edges[(parent, vertice)][0]))
                self.wait(0.2)
            self.play(Create(manim_graph.vertices[vertice][0]))
            self.wait(0.2)
            
            added_vertices.add(vertice)

            if not graph_dict[vertice]:
                change_label_to_value(vertice)

    
            if parent and all_descendants_added(parent, added_vertices, graph_dict):
                change_label_to_value(parent)
 
        change_label_to_value("2_depth_0")
        self.wait()


class AlphaBetaPruning(Scene):
    def construct(self):

        self.camera.background_color = GRAY_A

        graph_dict = {
            "2_depth_0": ["2_depth_1", "-4_depth_1"],
            "2_depth_1": ["4_depth_2", "2_depth_2"],
            "-4_depth_1": ["-4_depth_2", "-2_depth_2"],
            "4_depth_2": [],
            "2_depth_2": [],
            "-2_depth_2": [],
            "-4_depth_2": []
        }

        vertices = list(graph_dict.keys())
        edges = [(parent, child) for parent, children in graph_dict.items() for child in children]

        even_depth_nodes_colors = {node: "WHITE" for node in graph_dict.keys() if int(node[-1]) % 2 == 0}
        odd_depth_nodes_colors = {node: "BLACK" for node in graph_dict.keys() if int(node[-1]) % 2 != 0}

        vertices_colors = even_depth_nodes_colors | odd_depth_nodes_colors
        vertices_labels = {node: int(node.split("_")[0]) for node in graph_dict.keys()}

        vertex_config = {
            vertex: {
                "fill_color": vertices_colors[vertex],
                "value": vertices_labels[vertex],
                "label_color": "WHITE" if vertices_colors[vertex] == "BLACK" else "BLACK"
            } for vertex in vertices
        }
        labels = {v: Text("?", color="BLACK" if int(v[-1]) % 2 == 0 else "WHITE") for v in vertices}

        manim_graph = DiGraph(
            vertices,
            edges=edges[::-1],
            layout="tree",
            root_vertex="2_depth_0",
            vertex_config={
                v: {"fill_color": vertex_config[v]["fill_color"]}
                for v in vertex_config
            },
            labels=labels
        )

        # Alpha and Beta display text
        alpha_text = MathTex(r"Alpha = -\infty", font_size=48, color=BLACK).next_to(manim_graph, LEFT, buff=1)
        beta_text = MathTex(r"Beta = \infty", font_size=48, color=BLACK).next_to(alpha_text, DOWN, buff=0.5)
        self.play(Write(alpha_text), Write(beta_text))

        def update_alpha_beta_text(alpha, beta):
            alpha_str = r"Alpha = " + (r"-\infty" if alpha == float("-inf") else str(alpha))
            beta_str = r"Beta = " + (r"\infty" if beta == float("inf") else str(beta))

            new_alpha_text = MathTex(alpha_str, font_size=48, color=BLACK).move_to(alpha_text.get_center())
            new_beta_text = MathTex(beta_str, font_size=48, color=BLACK).move_to(beta_text.get_center())
            self.play(Transform(alpha_text, new_alpha_text), Transform(beta_text, new_beta_text))

        def alpha_beta(vertex, depth, alpha, beta, maximizing_player):
            """
            Alpha-beta pruning logic with animation.
            """
            self.play(Create(manim_graph.vertices[vertex][0]))
            label = labels[vertex]
            if not graph_dict[vertex]:  # Leaf node
                value = vertex_config[vertex]["value"]
                new_label = Text(str(value), color=vertex_config[vertex]["label_color"])
                new_label.move_to(manim_graph[vertex].get_center())
                self.play(Transform(label, new_label))
                return value

            if maximizing_player:
                max_eval = float("-inf")
                for child in graph_dict[vertex]:
                    self.play(Create(manim_graph.edges[(vertex, child)][0]))
                    self.wait(0.2)

                    eval = alpha_beta(child, depth + 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    update_alpha_beta_text(alpha, beta)

                    if beta <= alpha:
                        # Prune the remaining children
                        break

                # Update the label with the max value
                new_label = Text(str(max_eval), color=vertex_config[vertex]["label_color"])
                new_label.move_to(manim_graph[vertex].get_center())
                self.play(Transform(label, new_label))
                return max_eval
            else:
                min_eval = float("inf")
                for child in graph_dict[vertex]:
                    self.play(Create(manim_graph.edges[(vertex, child)][0]))
                    self.wait(0.2)

                    eval = alpha_beta(child, depth + 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    update_alpha_beta_text(alpha, beta)

                    if beta <= alpha:
                        # Prune the remaining children
                        break

                # Update the label with the min value
                new_label = Text(str(min_eval), color=vertex_config[vertex]["label_color"])
                new_label.move_to(manim_graph[vertex].get_center())
                self.play(Transform(label, new_label))
                return min_eval

        # Start the alpha-beta pruning
        alpha_beta("2_depth_0", 0, float("-inf"), float("inf"), True)
        self.wait()

