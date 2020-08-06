import maze
import Maze_Solver


class Maze_Generator:

    solving_mode = {"random": Maze_Solver.Random_Solver}
    def __init__(self, height:int, width:int, generation_mode:str, solving_strategy:str=False):

        self.maze = maze.Maze(height, width, generation_mode)

        if solving_strategy:
            self.solver = self.solving_mode[solving_strategy](self.maze)


    def get_maze(self):
        return self.maze

    def get_solver(self):
        return self.solver