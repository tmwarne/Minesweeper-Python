from tkinter import *
from classes import Board

root = Tk()

board = Board()

buttons = []
for i in range(board.y):
        row=[]
        for j in range(board.x):
            row.append(Button(root, background="gray", text="      ", disabledforeground="black"))
            row[j].grid(row=j,column=i)  
        buttons.append(row)


def check_square(x, y, board):
    if board.squares[x][y].is_clicked or board.squares[x][y].is_flagged:
        return
    board.squares[x][y].click()
    if board.squares[x][y].is_mine:
        lose_game(board)
        return
    elif board.squares[x][y].adjacent == 0:
        buttons[x][y].config(text="  0  ")
        buttons[x][y]["state"] = "disabled"
        x_adj = [x-1, x, x+1]
        y_adj = [y-1, y, y+1]
        for i in y_adj:
            for j in x_adj:
                if (0<=i<=9 and 0<=j<=9 and not board.squares[j][i].is_clicked):
                    check_square(j, i, board)
    else:
        check_state(board)
        buttons[x][y].config(text="  " + str(board.squares[x][y].adjacent) + "  ")
        buttons[x][y]["state"] = "disabled"
        return


def right_click(event):
    grid_info = event.widget.grid_info()
    if not board.squares[grid_info["column"]][grid_info["row"]].is_flagged:
        event.widget.configure(bg="red")
        board.squares[grid_info["column"]][grid_info["row"]].flag()
        event.widget["state"] = "disabled"
    else:
        event.widget.configure(bg="gray")
        board.squares[grid_info["column"]][grid_info["row"]].un_flag()
        event.widget["state"] = "normal"


def lose_game(board):
    for y in range(board.y):
        for x in range(board.x):
            buttons[x][y].config(text="  *  ")
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="red")


def win_game(board):
    for y in range(board.y):
        for x in range(board.x):
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="green")
            if board.squares[x][y].is_mine:
                buttons[x][y].config(text="  *  ")


def check_state(board):
    total = (board.x*board.y)-board.mines
    count=0
    for y in range(board.y):
        for x in range(board.x):
            if board.squares[x][y].is_clicked:
                count+=1
    if count < total:
        return
    else:
        win_game(board)
                



for i in range(board.y):
    for j in range(board.x):
        buttons[j][i].config(command=lambda i=i, j=j: check_square(j, i, board))
        buttons[j][i].bind("<Button-2>", right_click)
        buttons[j][i].bind("<Button-3>", right_click) 
        
root.mainloop()