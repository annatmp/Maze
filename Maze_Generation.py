import maze
import Maze_Solver


class Maze_Generator:
    def __init__(self, height:int, width:int, generation_mode:str, solving_strategy:str=False):

        self.maze = maze.Maze(height, width, generation_mode)

        if solving_strategy:
            self.solver = Maze_Solver.Maze_Solver(self.maze, solving_strategy)

    def get_maze(self):
        return self.maze