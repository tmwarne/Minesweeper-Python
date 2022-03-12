import random

class Square:
    def __init__(self):
        self.is_mine=False
        self.adjacent=0
        self.is_flagged=False
        self.is_clicked=False

    def set_mine(self):
        self.is_mine=True

    def click(self):
        self.is_clicked=True
    
    def flag(self):
        self.is_flagged=True

    def un_flag(self):
        self.is_flagged=False

    def set_adj(self, adj):
        self.adjacent=adj


class Board:
    def __init__(self, x=10, y=10, mines=10):
        self.squares=[]
        self.x=x
        self.y=y
        self.mines=mines
        for i in range(self.y):
            row=[]
            for j in range(self.x):
                row.append(Square())
            self.squares.append(row)
        coordinates=self.generate_mine_locations(self.x, self.y, self.mines)
        for loc in coordinates:
            self.squares[loc[1]][loc[0]].set_mine()
        self = self.calc_adjacencies(self.x, self.y)


    def generate_mine_locations(self, x=10, y=10, mines=10):
        coordinates=[]
        while len(coordinates) < mines:
            x_coord = random.randint(0,x-1)
            y_coord = random.randint(0,y-1)
            if ((x_coord, y_coord)) not in coordinates:
                coordinates.append((x_coord, y_coord))
        return coordinates


    def calc_adjacencies(self, x, y):
        for i in range(y):
            for j in range(x):
                count=0
                x_adj = [j-1, j, j+1]
                y_adj = [i-1, i, i+1]
                for k in y_adj:
                    for l in x_adj:
                        if (0<=k<=self.y-1 and 0<=l<=self.x-1):
                            if self.squares[k][l].is_mine == True:
                                count+=1
                self.squares[i][j].set_adj(count)
        return self