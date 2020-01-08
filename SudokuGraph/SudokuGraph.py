import networkx as nx
import itertools
import random
import csv

DEFAULT_WIDTH = 9
DEFAULT_HEIGHT = 9
DEFAULT_GRID_WIDTH = 3
DEFAULT_GRID_HEIGHT = 3

class SudokuGraph(nx.Graph):
    def __init__(self):
        super().__init__()
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.grid_width = DEFAULT_GRID_WIDTH
        self.grid_height = DEFAULT_GRID_HEIGHT

    def create_nodes(self):
        for n in range(0, self.width*self.height):
            i = n // self.width
            j = n % self.width

            self.add_node((i, j))

    def connect_all_nodes(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                node = (i, j)
                self.connect_column_to(node)
                self.connect_row_to(node)
                self.connect_grid_to(node)

    def connect_column_to(self, node):
        for other_i in range(0, self.height):
            if other_i != node[0]:
                other_n = (other_i, node[1])
                self.add_edge(node, other_n)

    def connect_row_to(self, node):
        for other_j in range(0, self.width):
            if other_j != node[1]:
                other_n = (node[0], other_j)
                self.add_edge(node, other_n)


    def connect_grid_to(self, node):
        m = node[1] // self.grid_width
        l = node[0] // self.grid_height

        for grid_i in range(l*self.grid_height, self.grid_height*(l+1)):
            for grid_j in range(m * self.grid_height, self.grid_height * (m + 1)):
                if grid_i != node[0] and grid_j != node[1]:
                    self.add_edge(node, (grid_i, grid_j))

    def load_tsv(self, filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file, delimiter='\t')
            rows = list(reader)
            for i in range(0, len(rows)):
                for j in range(0, len(rows[i])):
                    val = 'x'
                    try:
                        val = int(rows[i][j]) -1
                    except ValueError as e:
                        repr(e)
                    self.nodes[(i, j)]['value'] = val
    def save_tsv(self, filename):
        with open(filename, 'w', newline='\n') as file:
            for i in range(0, self.height):
                for j in range(0, self.width):
                    val = 'x'
                    if isinstance(self.nodes[(i, j)]['value'], int):
                        val = self.nodes[(i, j)]['value'] +1
                    file.write(f"{val}\t")
                file.write('\n')


    def solve(self):
        values = {k: v['value'] for k, v in self.nodes(data=True) if isinstance(v['value'], int)}
        counts = {self.width:0}
        colors = {}
        while self.width in counts:
            colors = {}
            counts = {}
            shuffled = list(range(0, self.width))
            random.shuffle(shuffled)
            nodes = nx.algorithms.coloring.strategy_connected_sequential_bfs(self, values)
            for u, val in values.items():
                counts[val] = counts.get(val, 0) + 1
                colors[u] = val
            for u in nodes:
                if u not in values:
                    # Set to keep track of colors of neighbours
                    neighbour_colors = {colors[v] for v in self[u] if v in colors}
                    # Find the first unused color.
                    iters = itertools.chain(shuffled, itertools.count(self.width))
                    for color in iters:
                        if color not in neighbour_colors:
                            break
                    # Assign the new color to the current node.
                    counts[color] = counts.get(color, 0) + 1
                    colors[u] = color
            print(counts)

        for k, v in colors.items():
            self.nodes[k]['value'] = v

if __name__ == '__main__':
    G= SudokuGraph()
    G.create_numbers()
    G.connect_all_nodes()
    G.load_tsv('9x9-00.tsv')
    G.solve()
    G.save_tsv('saved.tsv')