import unittest
from .SudokuGraph import *

class TestCreation(unittest.TestCase):
    def setUp(self) -> None:
        self.graph = SudokuGraph()

    def test_classtype(self):
        self.assertIsInstance(self.graph, nx.Graph)

    def test_nodecount(self):
        self.assertEqual(len(self.graph.nodes()), self.graph.width * self.graph.height)

if __name__ == '__main__':
    unittest.main()
