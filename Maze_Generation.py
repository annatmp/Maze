import Maze
import Maze_Solver


class Maze_Generator:

    solving_mode = {"random": Maze_Solver.Random_Solver}
    def __init__(self, height: int, width: int, generation_mode: str, solving_strategy: str = False):

        self.maze = Maze.Maze(height, width, generation_mode)

        if solving_strategy:
            self.solver = self.generate_solution(solving_strategy)
            self.solution = self.solver.walker

    def generate_maze(self,height, width, generation_mode):
        try:
            maze = Maze.Maze(height, width, generation_mode)
            return maze
        except RecursionError:
            # in case we hit the recursion depth just start over new, mostly a new attempt finds it
            print("Recursion depth hit during maze generation, start new")
            self.generate_maze(height, width, generation_mode)

    def generate_solution(self,solving_strategy):
        try:
            solver = self.solving_mode[solving_strategy](self.maze)
            return solver
        except RecursionError:
            # in case we hit the recursion depth just start over new, mostly a new attempt finds it
            print("Recursion depth hit during solution generation, start new")
            self.generate_solution(solving_strategy)

    def get_maze(self):
        return self.maze

    def get_solver(self):
        return self.solver