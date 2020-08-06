import maze



class Maze_Generator:
    def __init__(self, height:int, width:int, generation_mode:str, solving_strategy:str=False):

        self.maze = maze.Maze(height, width, generation_mode)

    def get_maze(self):
        return self.maze