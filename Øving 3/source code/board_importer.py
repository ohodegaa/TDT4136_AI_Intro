__author__ = 'ohodegaa'

import os

# directory path of current project
project_dir = os.path.abspath(os.path.dirname(__file__))


# directory named "boards" should be placed in this (project_dir) directory


class BoardImporter:
    def __init__(self, path: str = "/boards"):
        self.board_dir = project_dir + path
        self.all_boards = []
        for board in os.listdir(self.board_dir):
            if board.startswith("board") and board.endswith(".txt"):
                self.all_boards.append(board)

    def boards_for_part(self, part: int):
        boards_for_part = []

        for board in self.all_boards:
            if board.startswith("board-{}".format(part)):
                boards_for_part.append(self.board_dir + "/" + board)

        return boards_for_part

    def get_board(self, part, board):
        part_boards = self.boards_for_part(part)

        _board = []
        for board_path in part_boards:
            if board_path.endswith("board-{}-{}.txt".format(part, board)):
                board_file = open(board_path, 'r')
                for line in board_file.readlines():
                    _board.append([x for x in line.strip()])

                board_file.close()
                break

        return _board

imp = BoardImporter()
imp.get_board(1, 1)
