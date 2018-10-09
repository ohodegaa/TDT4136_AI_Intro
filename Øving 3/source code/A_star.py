from board_builder import *
from heapq import *




class AStar:
    def __init__(self, part=1, board=1):
        self.board = Board(part, board)
        self.closed_list = []
        self.open_list = []
        self.graphic_board = GraphicBoard(self.board)

    def search(self, algorithm="A-star"):
        self.board.start.gscore = 0
        h = self.board.start.heuristic(self.board.goal)
        self.board.start.fscore = self.board.start.gscore + h
        self.open_list.append(self.board.start)

        self.open_total = []


        while True:
            if len(self.open_list) <= 0:
                return "Failed to find path"


            # find the cheapest node in open list
            min_node = self.open_list[0]
            for x in self.open_list:
                if algorithm == "A-star":
                    if x.fscore < min_node.fscore:
                        min_node = x
                elif algorithm == "Dijkstra":
                    if x.gscore < min_node.gscore:
                        min_node = x
                elif algorithm == "BFS":
                    min_node = self.open_list[0]
                    break
            node = min_node
            self.open_list.remove(min_node)
            self.closed_list.append(node)

            # if a solution is found:
            if node.sign == self.board.goal.sign:
                solution = self.solution(node)
                self.graphic_board.draw_board(solution, self.open_list, self.closed_list)
                return solution

            # find successors
            successors = self.board.successors(node)
            node.kids.extend(successors)

            # find the cheapest successor and update costs
            for successor in successors:


                if successor not in self.closed_list + self.open_list:
                    self.attach_and_eval(successor, node)
                    self.open_list.append(successor)
                    if successor not in self.open_total:
                        self.open_total.append(successor)

                # if path through "node" to successor is cheaper than previous
                elif node.gscore + successor.arc_cost() < successor.gscore:
                    self.attach_and_eval(successor, node)
                    if successor in self.closed_list:
                        self.propagate_path_improvements(successor)

    def attach_and_eval(self, child, parent):
        child.parent = parent
        child.gscore = parent.gscore + child.arc_cost()
        child.fscore = child.gscore + child.heuristic(self.board.goal)

    def propagate_path_improvements(self, parent):
        for kid in parent.kids:
            if parent.gscore + parent.arc_cost() < kid.gscore:
                kid.parent = parent
                kid.gscore = parent.gscore + kid.arc_cost()
                kid.fscore = kid.gscore + kid.heuristic(self.board.goal)
                self.propagate_path_improvements(kid)

    def solution(self, node):
        if node.parent is None:
            return [node]
        else:
            return [node] + self.solution(node.parent)


test_boards = [[1, 1], [1, 2], [1, 3], [1, 4], [2, 1], [2, 2], [2, 3], [2, 4]]

algorithm = input("which algorithm? (1 = A-star, 2=Dijkstra, 3=BFS")

algorithms = {
    "1": "A-star",
    "2": "Dijkstra",
    "3": "BFS"
}

for board in test_boards:
    astar = AStar(board[0], board[1])
    astar.search(algorithms.get(algorithm, "A-star"))


"""



"""