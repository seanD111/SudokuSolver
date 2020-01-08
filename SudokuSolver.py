from solving_functions import solve_sudoku
import csv
import copy

DEFAULT_WIDTH = 9
DEFAULT_HEIGHT = 9
DEFAULT_GRID_WIDTH = 3
DEFAULT_GRID_HEIGHT = 3

class SudokuSolver():
    def __init__(self):
        self.width = DEFAULT_WIDTH
        self.height = DEFAULT_HEIGHT
        self.grid_width = DEFAULT_GRID_WIDTH
        self.grid_height = DEFAULT_GRID_HEIGHT
        self.rows_in = None
        self.rows_out = None


    def load_tsv(self, filename):
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file, delimiter='\t')
            self.rows_in = [[int(val) for val in row] for row in reader]

    def save_tsv(self, filename):
        with open(filename, 'w', newline='\n') as file:
            writer = csv.writer(file, delimiter='\t')
            writer.writerows(self.rows_out)


    def solve(self):
        grid = copy.deepcopy(self.rows_in)
        self.rows_out =  list(solve_sudoku((self.grid_width, self.grid_height), grid))[0]

if __name__ == '__main__':
    S = SudokuSolver()
    S.load_tsv('9x9-01.tsv')
    S.solve()
    S.save_tsv('9x9-01soln.tsv')
    pass
