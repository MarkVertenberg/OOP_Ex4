
import unittest
from DiGraph import Node
from GraphAlgo import GraphAlgo
from pokemon import Pokemon
from agent import Agent


# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

class MyTestCase(unittest.TestCase):
    def test_Node(self):
        node1 = Node(1, (1.0, 2.0))
        node2 = Node(2, (1.0, 8.0))
        self.assertEqual(1, node1.get_value())
        self.assertEqual(2, node2.get_value())
        self.assertEqual(1.0, node1.get_x())
        self.assertEqual(1.0, node2.get_x())
        self.assertEqual(2.0, node1.get_y())
        self.assertEqual(8.0, node2.get_y())
        self.assertEqual(6.0, node1.distance(node2))

    def test_DiGraph(self):
        test_graph = GraphAlgo()
        test_graph.load_from_json('../data/A0.json')
        self.assertEqual(test_graph.graph.v_size(), 11)
        self.assertEqual(test_graph.graph.e_size(), 22)
        self.assertEqual(len(test_graph.graph.get_all_v()), 11)
        self.assertEqual(len(test_graph.graph.all_in_edges_of_node(0)), 2)
        self.assertEqual(len(test_graph.graph.all_out_edges_of_node(0)), 2)
        test_graph.graph.add_edge(0, 2, 3)
        self.assertEqual(test_graph.graph.Lines[(0, 2)], 3)
        self.assertEqual(test_graph.graph.get_mc(), 34)
        test_graph.graph.add_node(18, (35.21310882485876, 32.104636394957986, 0.0))
        self.assertEqual(test_graph.graph.v_size(), 12)
        self.assertEqual(True, test_graph.graph.remove_node(18))
        self.assertEqual(True, test_graph.graph.remove_edge(0, 1))
        self.assertEqual(False, test_graph.graph.remove_edge(0, 1))

    def test_GraphAlgo(self):
        test_graph = GraphAlgo()
        self.assertTrue(test_graph.load_from_json('../data/A0.json'))
        self.assertTrue(test_graph.save_to_json("saved_file.json"))
        test_graph2 = GraphAlgo()
        test_graph2.graph.add_node(0)
        test_graph2.graph.add_node(1)
        test_graph2.graph.add_node(2)
        test_graph2.graph.add_edge(0, 1, 2)
        test_graph2.graph.add_edge(1, 2, 3)
        self.assertEqual(test_graph2.shortest_path(0, 1), (2, [0, 1]))
        self.assertEqual(test_graph2.shortest_path(0, 2), (5, [0, 1, 2]))
        test_graph2.graph.remove_node(1)
        self.assertEqual(test_graph2.shortest_path(0, 2), (float('inf'), []))
        self.assertEqual(test_graph.centerPoint(), (7, 6.806805834715163))
        path = [1, 4, 7, 3, 6]
        expected = ([1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 4, 5, 6], 19.012874172166818)
        self.assertEqual(expected, test_graph.TSP(path))

    def test_game(self):
            test_graph = GraphAlgo()
            test_graph.load_from_json('../data/A0')
            node1 = Node(1, (1.0, 2.0))
            node2 = Node(2, (5.0, 4.0))
            node3 = Node(3, (2.0, 6.0))
            node4 = Node(4, (9.0, 6.0))
            pok = {"value": 5.0,
                    "type": -1,
                    "pos": "32.197656770719604,37.10191878639921,0.0"}
            pok1 = {"value": 6.0,
                   "type": -1,
                   "pos": "31.197656770719604,33.10191878639921,0.0"}
            pok2 = {"value": 7.0,
                    "type": -1,
                    "pos": "39.197656770719604,33.10191878639921,0.0"}
            pok3 = {"value": 8.0,
                    "type": -1,
                    "pos": "34.197656770719604,30.10191878639921,0.0"}
            poki = Pokemon(pok)
            poki1 = Pokemon(pok)
            poki2 = Pokemon(pok)
            poki3 = Pokemon(pok)
            dis = Pokemon.dist_pok_from_ver(poki, node1)
            dis1 = Pokemon.dist_pok_from_ver(poki1, node2)
            dis2 = Pokemon.dist_pok_from_ver(poki2, node3)
            dis3 = Pokemon.dist_pok_from_ver(poki3, node1)
            self.assertEqual(46.96209631682334, dis)
            self.assertEqual(42.842147018552176, dis1)
            self.assertEqual(43.35006143753385, dis2)
            self.assertEqual(46.96209631682334, dis3)
            a = {
                "id": 0,
                "value": 0.0,
                "src": 0,
                "dest": 1,
                "speed": 3.0,
                "pos": "32.18753053591606,37.10378225882353,0.0"
            }
            b = {
                "id": 0,
                "value": 1.0,
                "src": 1,
                "dest": 3,
                "speed": 5.0,
                "pos": "31.18753053591606,36.10378225882353,0.0"
            }
            c = {
                "id": 0,
                "value": 2.0,
                "src": 1,
                "dest": 2,
                "speed": 4.0,
                "pos": "32.18753053591606,34.10378225882353,0.0"
            }
            ag = Agent(a)
            ag1 = Agent(b)
            ag2 = Agent(c)

            poki.src = 10
            dist_ag_to_pok = test_graph.shortest_path(ag.src, poki.src)[0]
            dist_ag_to_pok1 = test_graph.shortest_path(ag1.src, poki.src)[0]
            dist_ag_to_pok2 = test_graph.shortest_path(ag2.src, poki.src)[0]
            self.assertEqual(float("inf"), dist_ag_to_pok)
            self.assertEqual(float("inf"), dist_ag_to_pok1)
            self.assertEqual(float("inf"), dist_ag_to_pok2)

            """   g = game()
            g.client.start_connection(HOST, PORT)
            g.client.add_agent("{\"id\":0}")
            g.client.add_agent("{\"id\":1}")
            g.client.add_agent("{\"id\":2}")
            g.client.add_agent("{\"id\":3}")
            file_location = '../data/graph_file_json'
            with open(file_location, 'w') as f:
             f.write(g.client.get_graph())
             g.graph_algo.load_from_json(file_location)
             g.client.start()
             g.find_src_dest_of_pok(poki)
            exit(0)"""


if __name__ == '__main__':
    unittest.main()
