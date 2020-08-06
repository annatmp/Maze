from maze import Maze
import random
from Cell import Cell

class Maze_Solver:

    SOLVING_ALGORITHMS = ["random"]

    def __init__(self,maze:Maze,solving_strategy):
        self.maze = maze
        self.execute_strategy = {"random" : self.random_search,"wall_flower" : self.wall_flower}
        self.execute_strategy[solving_strategy]()

    def random_search(self):
        """
        random maze solving, backtracks when hitting a wall. Stores the "dead" ends
        UNINFORMED!
        """
        print("enter random search")
        path = []
        dead_ends = []

        # get the details from the maze
        start = self.maze.get_start()
        assert(isinstance(start,Cell))

        #set start as the first cell in the path
        path.append(start)

        def move(path, dead_ends):
            #import pdb; pdb.set_trace()
            possible_directions = self.get_possible_directions(path[-1])
            if len(possible_directions) == 1 and not len(path) == 1:
                # if we are not at the start and there is only one way to go, we are in a dead end.
                dead_ends.append(path.pop())
                move(path,dead_ends)
            else:
                #check if any of the direction is a dead end
                not_visited_directions = [cell for cell in possible_directions if cell not in dead_ends]
                if len(not_visited_directions) == 0:
                    #continue to backtrack
                    dead_ends.append(path.pop())
                    move(path,dead_ends)

                else:
                    direction = random.choice(not_visited_directions)

                    neighbour = self.maze.get_neighbour_by_direction(path[-1],direction)
                    path.append(neighbour)
                    #check if cell is end cell
                    if neighbour.isEnd:
                        print("Found solution")
                        return path, dead_ends
                    else:
                        print(neighbour)
                        move(path, dead_ends)

        # start moving
        move(path,dead_ends)


    def get_possible_directions(self,cell:Cell):
        walls = cell.get_walls()
        possible_directions = [direction for direction,wall in walls.items() if not wall]
        return possible_directions

    def wall_flower(self):
        pass
