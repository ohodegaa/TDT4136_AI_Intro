__author__ = 'ohodegaa'
import time
import pygame
from board_importer import BoardImporter

INFINITE = float('inf')

weights = {
    '.': 1,
    '#': INFINITE,
    'A': 0,
    'B': 0,
    'w': 100,
    'm': 50,
    'f': 10,
    'g': 5,
    'r': 1,
}


class Node:
    def __init__(self, sign, row, col):
        self.gscore = INFINITE
        self.fscore = INFINITE
        self.sign = sign
        self.weight = weights.get(sign)
        self.row = row
        self.col = col
        self.kids = []
        self.parent = None
        self.closed = False

    def __lt__(self, neighbor):
        return self.fscore < neighbor.fscore

    def heuristic(self, goal_node):
        def euclidean_distance(start, goal):
            return (start.col - goal.col) ** 2 + (start.row - goal.row) ** 2

        def manhattan_distance(start, goal):
            return abs(start.col - goal.col) + abs(start.row - goal.row)

        return manhattan_distance(self, goal_node)

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    """
    def __repr__(self):
        return "{}".format(self.sign)
    """

    def arc_cost(self):
        return self.weight or 1


class Board:
    def __init__(self, part, board):
        board_builder = BoardImporter()
        raw_board = board_builder.get_board(part, board)
        self.rows = len(raw_board)
        self.cols = len(raw_board[0])
        self.board = [[None for i in range(self.cols)] for j in range(self.rows)]
        self.start = None
        self.goal = None
        self.build_nodes(raw_board)

    def __len__(self):
        return len(self.board)

    def __getitem__(self, index):
        return self.board[index] if self.board else 0

    def build_nodes(self, board):

        for i in range(len(board)):
            for j in range(len(board[i])):
                node = Node(board[i][j], i, j)
                if board[i][j] == "A":
                    self.start = node
                elif board[i][j] == "B":
                    self.goal = node

                self.board[i][j] = node

    def successors(self, node):
        coordinates = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        neights = []
        for i in range(len(coordinates)):
            row_neighbor = node.row + coordinates[i][0]
            col_neighbor = node.col + coordinates[i][1]
            if self.valid_neighbor(row_neighbor, col_neighbor):
                neights.append(self.board[row_neighbor][col_neighbor])
        return neights

    def valid_neighbor(self, row, col):
        upper_bound = row >= 0
        lover_bound = row < len(self.board)
        left_bound = col >= 0
        right_bound = col < len(self.board[0])
        try:
            not_obstacle = self.board[row][col].sign != "#"
        except IndexError:
            return False
        return left_bound and right_bound and lover_bound and upper_bound and not_obstacle


class GraphicBoard:
    def __init__(self, board: Board):
        if board is not None:
            self.board = board
        else:
            raise Exception("Need a board (matrix) to draw graphics!")

        # constant sizes:
        self.CELL_SIZE = 25
        self.MARGIN = 3
        self.WIDTH = (self.MARGIN + self.CELL_SIZE) * len(board[0]) + self.MARGIN
        self.HEIGHT = (self.MARGIN + self.CELL_SIZE) * len(board) + self.MARGIN

        # colors:
        self.OBSTACLE = (150, 150, 150)
        self.OPEN = (255, 255, 255)
        self.START = (255, 0, 0)
        self.GOAL = (0, 255, 0)

        self.WATER = (0, 0, 255)
        self.MOUNTAINS = (150, 150, 150)
        self.FORESTS = (0, 90, 0)
        self.GRASSLANDS = (190, 255, 190)
        self.ROADS = (180, 150, 0)

        self.SOLUTION_NODE = (0, 0, 0)

    # displaying solution

    def draw_board(self, solution=None, open_list=None, closed_list=None):

        screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption("A-star Algorithm")

        showing_solution = False
        k = len(solution) - 2
        if solution:
            showing_solution = True
        done = False
        while not done:
            if showing_solution:
                s = [solution[k].row, solution[k].col]
                self.board[s[0]][s[1]].sign = 'P'
                if k == 0:
                    showing_solution = False
                    time.sleep(10)
                    done = True
                k -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    color = {
                        '.': self.OPEN,
                        '#': self.OBSTACLE,
                        'A': self.START,
                        'B': self.GOAL,
                        'P': self.SOLUTION_NODE,
                        'w': self.WATER,
                        'm': self.MOUNTAINS,
                        'f': self.FORESTS,
                        'g': self.GRASSLANDS,
                        'r': self.ROADS,
                    }[(self.board[row][col]).sign]
                    pygame.draw.rect(screen,
                                     color,
                                     [(self.MARGIN + self.CELL_SIZE) * col + self.MARGIN,
                                      (self.MARGIN + self.CELL_SIZE) * row + self.MARGIN,
                                      self.CELL_SIZE,
                                      self.CELL_SIZE])

            time.sleep(0.05)

            pygame.display.flip()

        pygame.quit()
