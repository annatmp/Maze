import random
import sys


class Wall_Not_Found_Exception(Exception):
    pass

class Not_Neighbour_Exception(Exception):
    pass

class Size_Limit_Exception(Exception):
    pass

class Cell:
    xpos: int
    ypos: int
    walls: {}
    visited: bool

    def __init__(self,xpos, ypos):

        self.xpos = xpos
        self.ypos = ypos
        self.visited = False #needed for generation
        self.isEnd = False
        self.walls = {"T": True, "B": True, "R": True, "L": True}


    def delete_wall(self,to_delete):
        #todo delete wall of neighbour?
        if not to_delete in self.walls.keys():
            raise Wall_Not_Found_Exception('{} cannot be deleted. Not a valid wall'.format(to_delete))

        self.walls.update({to_delete:False})

    def set_wall(self,to_set):

        if not to_set in self.walls.keys():
            raise Wall_Not_Found_Exception('{} cannot be created. Not a valid wall'.format(to_set))

        self.walls.update({to_set: True})

    def set_visited(self):

        self.visited = True

    def get_position(self):
        return (self.xpos, self.ypos)

    def vistited(self):
        return self.visited

    def set_end_cell(self):

        self.isEnd = True


    def get_walls(self):
       """
       @return walls, dict
       """
       return self.walls



    def __str__(self):

        return "{}/{}".format(self.xpos,self.ypos)


class Maze:

    GENERATION_ALGORITHMS = ["depth_first"]
    SOLVING_ALGORITHMS = ["test"]
    SIZE_LIMIT = 30

    def __init__(self, height:int, width:int, generation_mode:str):

        if height > self.SIZE_LIMIT or width > self.SIZE_LIMIT :
            raise Size_Limit_Exception("Maze size may not be bigger than {}".format(self.SIZE_LIMIT))
        self.height = height
        self.width = width
        self.mode = generation_mode
        self.cell_count = height*width
        self.cells = []
        self.ADJACENT_EDGES = {"T": "B", "R": "L", "B": "T", "L": "R"}

        self.generate()



    def generate(self):

        self.cells=[[Cell(x,y) for x in range(self.width)] for y in range(self.height)]

        if self.mode == "depth_first":
            self.depth_first_generation()

        elif self.mode == "test":
            pass

    def depth_first_generation(self):

        # start at random cell
        all_cells = [cell for cell in [row for row in self.cells]]
        random_cell = random.choice(all_cells)
        self.start = self.cells[0][0]
        queue = []
        path = []

        def rec(cell, path_length):
            #mark visited
            cell.set_visited()
            # push to queue
            queue.append(cell)
            # Get all non_visited neighbours
            not_seen_neigbours = [neighbour for neighbour in self.get_neighbours(cell) if not neighbour.visited]

            # if there is none
            if len(not_seen_neigbours) == 0:

                if len(queue) == 0:
                    return


                new_cell = queue.pop()
                path_length -= 1
                not_seen_prev_neigbours = [neighbour for neighbour in self.get_neighbours(new_cell)
                                           if not neighbour.visited]

                while (len(not_seen_prev_neigbours) == 0):

                    if len(queue) == 0:
                        return


                    new_cell = queue.pop()
                    path_length -= 1
                    not_seen_prev_neigbours = [neighbour for neighbour in self.get_neighbours(new_cell)
                                               if not neighbour.visited]

                cell = new_cell
                not_seen_neigbours = not_seen_prev_neigbours


            # delete the connecting wall between cell and not visited neighbour
            adjacent = random.choice(not_seen_neigbours)
            connecting_wall = self.get_wall(cell, adjacent)
            self.delete_cell_wall(cell, connecting_wall[0])

            # update path and start new
            path_length += 1
            path.append((adjacent,path_length))
            rec(adjacent,path_length)


        rec(self.start,0)
        #print("".join(["{}\n".format(cell) for cell in path]))

        path.sort(key=lambda x:x[1])

        self.end = path[-1][0]
        self.end.set_end_cell()
        self.path_length = path[-1][1]


        print(self.end)

    def delete_cell_wall(self,cell,wall):

        if not wall in self.ADJACENT_EDGES.keys():
            raise Wall_Not_Found_Exception("{} is not a valid wall".format(wall))


        cell.delete_wall(wall)
        xpos,ypos = cell.get_position()

        if wall == "T":
            neighbour = self.get_cell(xpos,ypos-1)
        elif wall == "B":
            neighbour = self.get_cell(xpos,ypos+1)
        elif wall == "R":
            neighbour = self.get_cell(xpos+1,ypos)
        else:
            neighbour = self.get_cell(xpos-1,ypos)

        neighbour.delete_wall(self.ADJACENT_EDGES[wall])

    def is_edge_cell(self,cell):

        xpos,ypos = cell.get_position()

        if xpos == 0 or ypos == 0 or xpos == self.width -1 or ypos == self.height-1:
            return True
        else:
            return False

    def get_wall(self, cell, neighbour):
        """
        @return: adjacent walls
        """
        xpos_c, ypos_c = cell.get_position()
        xpos_n, ypos_n = neighbour.get_position()

        if  xpos_c == xpos_n and ypos_c == ypos_n:
            raise Not_Neighbour_Exception("Same cell")

        elif xpos_c == xpos_n: #neigbour on same column
            if ypos_c - 1 == ypos_n:
                return ("T","B")
            elif ypos_c + 1 == ypos_n:
                return ("B","T")
            else:
                raise Not_Neighbour_Exception("Cells are not neighbouring")

        elif ypos_c == ypos_n: #neighbour on same row
            if xpos_c + 1 == xpos_n:
                return ("R", "L")
            elif xpos_c - 1 == xpos_n:
                return ("L","R")
            else:
                raise Not_Neighbour_Exception("Cells are not neighbouring")
        else:
            raise Not_Neighbour_Exception("Cells are not neighbouring")

    def get_neighbour_by_direction(self,cell:Cell, direction):
        #todo check that it is not the edge position
        position = cell.get_position()
        if direction == "T":
            neighbour = self.get_cell(position[0], position[1]-1)
        elif direction == "B":
            neighbour = self.get_cell(position[0], position[1]+1)
        elif direction == "R":
            neighbour = self.get_cell(position[0]-1, position[1])
        elif direction == "L":
            neighbour = self.get_cell(position[0]+1, position[1])
        else:
            neighbour = None

        return neighbour

    def get_neighbours(self,cell):

        xpos, ypos = cell.get_position()

        if not self.is_edge_cell(cell):
            neighbours = [self.get_cell(xpos,ypos-1), #top
                          self.get_cell(xpos+1,ypos), #right
                          self.get_cell(xpos,ypos+1), #bottom
                          self.get_cell(xpos-1,ypos)] #left

        #Edge cases:
        elif ypos == 0: # top row
            if xpos == 0: #0,0
                neighbours =    [self.get_cell(xpos+1,ypos), #right
                                 self.get_cell(xpos,ypos+1), #bottom
                                ]

            elif  xpos == self.width -1: #corner right top, no right
                neighbours = [self.get_cell(xpos, ypos+1),  # bottom
                              self.get_cell(xpos-1, ypos)] # left

            else: #top row, just no top position
                neighbours = [self.get_cell(xpos+1, ypos),  # right
                              self.get_cell(xpos, ypos + 1),  # bottom
                              self.get_cell(xpos-1, ypos)] #left


        elif xpos == 0:
            if ypos == self.height - 1:
                neighbours = [self.get_cell(xpos, ypos-1), #top
                              self.get_cell(xpos+1, ypos)]  # right
            else:
                neighbours = [self.get_cell(xpos, ypos-1),  # top
                              self.get_cell(xpos+1, ypos),  # right
                              self.get_cell(xpos, ypos+1)]  # bottom


        elif ypos == self.height-1:


            if xpos == self.width -1:
                neighbours = [self.get_cell(xpos,ypos-1), #top
                              self.get_cell(xpos-1,ypos)] #left

            else:
                neighbours = [self.get_cell(xpos, ypos-1),  # top
                              self.get_cell(xpos+1, ypos),  # right
                              self.get_cell(xpos-1, ypos)]  # left

        else:

            neighbours = [self.get_cell(xpos, ypos-1),  # top
                         self.get_cell(xpos, ypos+1),  # bottom
                         self.get_cell(xpos-1, ypos)]  # left


        return neighbours

    def get_cell(self,xpos,ypos):
        #this does run counterintuitive since the first number gives the row (and thus y coordinate) and
        # the second number the column (x coordinate)
        return self.cells[ypos][xpos]

    def get_cell_by_number(self,number):

        y = int(number / self.width)
        x = number % self.width

        return self.get_cell(x, y)

    def get_size(self):

        return (self.width,self.height)
  
    def create_solution_path(self):
        pass

    def get_cells(self):
        return self.cells

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def print(self):
        printer = Maze_printer(self.cells, self.start,self.end)
        printer.print()

    def get_mode_as_nice_string(self):
        mode_low_cap = self.mode.replace("_", " ")
        mode_all_cap = " ".join([word.capitalize() for word in mode_low_cap.split(" ")])
        return mode_all_cap

    def get_path_length(self):
        return self.path_length

    # @staticmethod
    # def supported_generation_mode():
    #
    #     return GENERATION_ALGORITHMS


    def __len__(self):
        """
        len of a maze is its number of cells
        :return:
        """
        return self.width * self.height


    def __str__(self):
        tmp = ""
        for row in self.cells:
            tmp += (" ".join(str(cell) for cell in row)) + '\n'
        return tmp

class Maze_printer:

    maze:Maze

    def __init__(self,maze_cells:list,start,end):

        self.maze = maze_cells
        self.maze_height = len(self.maze[1])
        self.maze_width = len(self.maze[0])
        self.start = start
        self.end = end

    def translate_to_string(self):

        representation = ""

        #top row
        representation += "".join(["+---" for i in range(self.maze_width)])
        representation += "+\n"

        #always append the right and bottom wall
        for index,row in enumerate(self.maze):

            vert = ["|"] #vertical lines
            hor = ["+"] #horizontal lines
            for cell in row:
                walls = cell.get_walls()

                if self.start == cell:
                    x = "o"
                elif self.end == cell:
                    x = "x"

                else:
                    x = " "

                if walls["R"]:
                    vert.append(" {} |".format(x))
                else:
                    vert.append(" {}  ".format(x))

                if walls["B"]:
                    hor.append("---+")
                else:
                    hor.append("   +")

            representation += "".join(vert)
            representation += "\n"
            representation += "".join(hor)
            representation += "\n"

        return representation

    def print(self):

        print(self.translate_to_string())



