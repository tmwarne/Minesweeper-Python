import random
from tkinter import *

root = Tk()

buttons = []
for i in range(10):
        row=[]
        for j in range(10):
            row.append(Button(root, background="gray", text="      ", disabledforeground="black"))
            row[j].grid(row=j,column=i)  
        buttons.append(row)


def build_board(x=10, y=10, mines=10):
    board=[]
    for i in range(y):
        i=[]
        for j in range(x):
            i.append(Square())
        board.append(i)
    coordinates=generate_mine_locations(x, y, mines)
    for loc in coordinates:
        board[loc[0]][loc[1]].set_mine()
    board = calc_adjacencies(x, y, board)
    return board


def generate_mine_locations(x=10, y=10, mines=10):
    coordinates=[]
    while len(coordinates) < mines:
        x_coord = random.randint(0,x-1)
        y_coord = random.randint(0,y-1)
        if ((x_coord, y_coord)) not in coordinates:
            coordinates.append((x_coord, y_coord))
    return coordinates


def calc_adjacencies(x, y, board):
    for i in range(y):
        for j in range(x):
            count=0
            x_adj = [j-1, j, j+1]
            y_adj = [i-1, i, i+1]
            for k in y_adj:
                for l in x_adj:
                    if (0<=k<=9 and 0<=l<=9):
                        if board[l][k].is_mine == True:
                            count+=1
            board[j][i].set_adj(count)
    return board


def check_square(x, y, board):
    if board[x][y].is_clicked or board[x][y].is_flagged:
        return
    board[x][y].click()
    if board[x][y].is_mine:
        lose_game()
        print(0)
        return 1
    elif board[x][y].adjacent == 0:
        buttons[x][y].config(text="  0  ")
        buttons[x][y]["state"] = "disabled"
        x_adj = [x-1, x, x+1]
        y_adj = [y-1, y, y+1]
        for i in y_adj:
            for j in x_adj:
                if (0<=i<=9 and 0<=j<=9 and not board[j][i].is_clicked):
                    check_square(j, i, board)
    else:
        check_state()
        buttons[x][y].config(text="  " + str(board[x][y].adjacent) + "  ")
        buttons[x][y]["state"] = "disabled"
        print(1)
        return 0


def right_click(event):
    grid_info = event.widget.grid_info()
    if not board[grid_info["column"]][grid_info["row"]].is_flagged:
        event.widget.configure(bg="red")
        board[grid_info["column"]][grid_info["row"]].flag()
        event.widget["state"] = "disabled"
    else:
        event.widget.configure(bg="gray")
        board[grid_info["column"]][grid_info["row"]].un_flag()
        event.widget["state"] = "normal"


def lose_game():
    for y in range(10):
        for x in range(10):
            buttons[x][y].config(text="  *  ")
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="red")


def win_game():
    for y in range(10):
        for x in range(10):
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="green")
            if board[x][y].is_mine:
                buttons[x][y].config(text="  *  ")


def check_state():
    total = 90
    count=0
    for y in range(10):
        for x in range(10):
            if board[x][y].is_clicked:
                count+=1
    if count < total:
        return
    else:
        win_game()
                

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


board = build_board()

for i in range(10):
    for j in range(10):
        buttons[j][i].config(command=lambda i=i, j=j: check_square(j, i, board))
        buttons[j][i].bind("<Button-2>", right_click)
        buttons[j][i].bind("<Button-3>", right_click) 
        
root.mainloop()