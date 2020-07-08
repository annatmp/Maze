import random


class Wall_Not_Found_Exception(Exception):
    pass

class Not_Neighbour_Exception(Exception):
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

        self.walls.update({to_delete:True})

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


    def __str__(self):

        return "{}/{}".format(self.xpos,self.ypos)


class Maze:

    ADJACENT_EDGES = {"T": "B", "R": "L", "B": "T", "L": "R"}
    height:int
    length:int
    start:Cell
    end:Cell
    mode:str
    cells:[]

    def __init__(self,height:int, width:int,mode:str):

        self.height = height
        self.width = width
        self.mode = mode
        self.cell_count = height*width

        self.generate()

    def generate(self):

        self.cells=[[Cell(x,y) for x in range(0,self.width)] for y in range(0,self.height)]


        if self.mode == "depth_first":
            self.depth_first_generation()


    def depth_first_generation(self):

        # start at random cell

        start = self.get_cell_by_number(random.randint(0,self.cell_count))



        def rec(cell):

            if cell.visited:
                return


            cell.set_visited()
            neighbours = self.get_neighbours(cell)

            random.shuffle(neighbours)

            for n in neighbours:
                if not n.visited:
                    connecting_wall = self.get_wall(cell,n)
                    cell.delete_wall(cell,connecting_wall)
                    rec(n)

        rec(start)


    def delete_cell_wall(self,cell,wall):

        if not wall in self.ADJACENT_EDGES.keys():
            raise Wall_Not_Found_Exception("{} is not a valid wall".format(wall))


        if not self.is_edge_cell(cell):
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

        xpos_c,ypos_c = cell.get_position()
        xpos_n, ypos_n = neighbour.get_position()

        if  xpos_c == xpos_n and ypos_c == ypos_n:
            raise Not_Neighbour_Exception("Same cell")

        elif xpos_c == xpos_n: #neigbour on same column
            if ypos_c + 1 == ypos_n:
                return ("T","B")
            elif ypos_c - 1 == ypos_n:
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




    def get_neighbours(self,cell):

        xpos, ypos = cell.get_position()

        neighbours = [self.get_cell(xpos,ypos+1), #top
                      self.get_cell(xpos+1,ypos), #right
                      self.get_cell(xpos,ypos-1), #bottom
                      self.get_cell(xpos-1,ypos-1)] #left

        return neighbours






    def get_cell(self,xpos,ypos):

        return self.cells[ypos][xpos]

    def get_cell_by_number(self,number):

        y = int(number / self.width)
        x = number % self.width

        return self.get_cell(x, y)






    def create_solution_path(self):
        pass



    def __str__(self):
        tmp = ""
        for row in self.cells:
            tmp += (" ".join(str(cell) for cell in row)) + '\n'
        return tmp



if __name__ == '__main__':

    maze = Maze(4,10,"depth_first")
    maze.get_cell_by_number(33)
    print(maze)





