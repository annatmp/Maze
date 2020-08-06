from maze import Maze
import random
from Cell import Cell
from Maze_Exceptions import No_Solution_Found_Exception
from Maze_Walk import Maze_Walk

def get_possible_directions(cell: Cell):
    walls = cell.get_walls()
    possible_directions = [direction for direction, wall in walls.items() if not wall]
    return possible_directions


class Maze_Solver:

    def __init__(self,maze):

        self.maze = maze
        self.walker = Maze_Walk(self.maze.get_start())


    def get_not_visited_neighbours_by_directions(self, cell, directions):

        valid_neighbours = {}
        for direction in directions:
            neighbour = self.maze.get_neighbour_by_direction(cell, direction)
            if not self.walker.was_visited(neighbour):
                valid_neighbours.update({direction: neighbour})

        return valid_neighbours

    def get_solution(self):
        return self.walker.full_solution_path()





class Random_Solver(Maze_Solver):

    SOLVING_ALGORITHMS = ["random"]

    def __init__(self,maze:Maze):
        super(Random_Solver, self).__init__(maze)
        self.solve()


    def solve(self):
        """
        random maze solving, backtracks when hitting a wall. Stores the "dead" ends
        UNINFORMED!
        """
        path = []


        # get the details from the maze
        start = self.maze.get_start()
        assert(isinstance(start,Cell))

        #set start as the first cell in the path

        def move():
            #import pdb; pdb.set_trace()
            current = self.walker.get_current()
            possible_directions = get_possible_directions(current)

            if len(possible_directions) == 1 and not self.walker.is_at_start():
                # if we are not at the start and there is only one way to go, we are in a dead end.
                self.walker.turn_back()
                move()
            else:
                #check if any of the direction is a dead end
                valid_neighbours = self.get_not_visited_neighbours_by_directions(current, possible_directions)

                if len(valid_neighbours) == 0:
                    #continue to backtrack
                    self.walker.turn_back()

                    if self.walker.is_at_start():
                        raise No_Solution_Found_Exception("Returned to Start without new options")
                    move()

                else:
                    direction = random.choice(list(valid_neighbours.keys()))
                    neighbour = valid_neighbours[direction]

                    self.walker.walk(neighbour, direction)

                    #check if cell is end cell
                    if neighbour.isEnd:
                        print("Found solution")
                        return

                    else:
                        move()


        # start moving
        move()



