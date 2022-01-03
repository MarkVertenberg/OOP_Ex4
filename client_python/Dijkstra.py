from typing import List

from GraphInterface import GraphInterface


class Dijkstra:
    """
        Implementation of Dijkstra’s algorithm for finding the shortest path
        between one node in a graph and another.
        Explanation of the algorithm can be found here: https://www.youtube.com/watch?v=pVfj6mxhdMw.
    """

    INFINITY = float('inf')

    def __init__(self):
        self.un_visited: List = []
        self.shortest_dist_from_src: dict = {}
        self.previous_node: dict = {}

    def reset(self, graph: GraphInterface, src_id: int):
        """ Updates the data to current graph and node. """
        self.un_visited = list(graph.get_all_v().keys())
        self.shortest_dist_from_src = {}
        self.previous_node = {}
        self.shortest_dist_from_src[src_id] = 0
        for node_id in self.un_visited:
            if node_id != src_id:
                self.shortest_dist_from_src[node_id] = self.INFINITY

    def do_algo(self, graph: GraphInterface, src_id: int):
        """ Dijkstra's algorithm """
        if graph is None or not graph.get_all_v().keys().__contains__(src_id):
            raise ValueError("source node not exist")
        self.reset(graph, src_id)
        while self.un_visited.__len__() != 0:
            curr_node = self.min_dist_in_un_visited()
            out_edges = graph.all_out_edges_of_node(curr_node)
            if out_edges:
                for dest in list(out_edges.keys()):
                    if self.un_visited.__contains__(dest):
                        total_dist_curr_to_dest = self.shortest_dist_from_src.get(curr_node) + out_edges[dest]
                        if total_dist_curr_to_dest < self.shortest_dist_from_src.get(dest):
                            self.shortest_dist_from_src[dest] = total_dist_curr_to_dest
                            self.previous_node[dest] = curr_node
            self.un_visited.remove(curr_node)

    def min_dist_in_un_visited(self):
        """ Finds the minimum distance to src from unvisited nodes """
        minimum = self.un_visited[0]
        for node in self.un_visited:
            if self.shortest_dist_from_src[node] < self.shortest_dist_from_src[minimum]:
                minimum = node
        return minimum

    def is_there_path(self, dest):
        """ Returns if there is path from src to dest
            Note: this function need to be used on graph that passed through the algorithm """
        if self.shortest_dist_from_src.get(dest) is not None:
            return self.shortest_dist_from_src[dest] != self.INFINITY
        raise ValueError("destination node not exist")

    def shortest_path(self, graph: GraphInterface, src: int, dest: int):
        """ Returns tuple that consists the distance and the path of the shortest path from src to dest """
        self.do_algo(graph, src)
        distance = self.INFINITY
        path = []
        if self.is_there_path(dest):
            distance = self.shortest_dist_from_src[dest]
            path = self.shortest_path_list(src, dest)
        return distance, path

    def shortest_path_list(self, src, dest):
        """ Returns list representing the shortest path from src to dest
            Note: this function need to be used on graph that passed through the algorithm """
        path = []
        curr_node = dest
        while curr_node != src:
            path.append(curr_node)
            curr_node = self.previous_node[curr_node]
        path.append(src)
        path.reverse()
        return path
