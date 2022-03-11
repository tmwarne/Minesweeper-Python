from tkinter import *
from classes import Board
import threading

#Create initial board and global variables
board = Board()
flag_count=0
timer=0

#Create GUI resources
root = Tk()
root.title(string='MINESWEEPER')
button_frame = Frame(root)
button_frame.pack( side = BOTTOM, fill='x', expand=True )
control_frame = Frame(root)
control_frame.pack(side = TOP, fill="x", expand=True)
new_button = Button(control_frame, background="light gray", text="New Game")
new_button.grid(row=0, column=1, sticky='ew')
flag_label = Label(control_frame, text=str(board.mines))
flag_label.grid(row=0, column=0, sticky='ew')
time_label = Label(control_frame, text=str(timer))
time_label.grid(row=0, column=2, sticky='ew')
control_frame.columnconfigure(0, weight=1)
control_frame.columnconfigure(1, weight=0)
control_frame.columnconfigure(2, weight=1)

#Function to set up 2D array of buttons and attach to the GUI 
buttons = []
for i in range(board.y):
        row=[]
        for j in range(board.x):
            row.append(Button(button_frame, background="gray", text="      ", disabledforeground="black", height=1, width=2))
            row[j].grid(row=j,column=i, sticky='ew')  
        buttons.append(row)

#Logic for when a game square is pressed 
def check_square(x, y, board):
    if board.squares[x][y].is_clicked or board.squares[x][y].is_flagged:
        return
    board.squares[x][y].click()
    if board.squares[x][y].is_mine:
        lose_game(board)
        return
    elif board.squares[x][y].adjacent == 0:
        buttons[x][y].configure(bg="LightGrey")
        buttons[x][y]["state"] = "disabled"
        x_adj = [x-1, x, x+1]
        y_adj = [y-1, y, y+1]
        for i in y_adj:
            for j in x_adj:
                if (0<=i<=9 and 0<=j<=9 and not board.squares[j][i].is_clicked):
                    check_square(j, i, board)
    else:
        buttons[x][y].config(text="  " + str(board.squares[x][y].adjacent) + "  ")
        buttons[x][y]["state"] = "disabled"
        buttons[x][y].configure(bg="LightGrey")
        check_state(board)
        return


#Logic for right clicking (flag/unflag)
def right_click(event):
    global flag_count
    grid_info = event.widget.grid_info()
    if board.squares[grid_info["column"]][grid_info["row"]].is_clicked:
        return
    if not board.squares[grid_info["column"]][grid_info["row"]].is_flagged:
        event.widget.configure(bg="red")
        board.squares[grid_info["column"]][grid_info["row"]].flag()
        event.widget["state"] = "disabled"
        flag_count+=1
        flag_label.config(text=str(board.mines - flag_count))
    else:
        event.widget.configure(bg="gray")
        board.squares[grid_info["column"]][grid_info["row"]].un_flag()
        event.widget["state"] = "normal"
        flag_count-=1
        flag_label.config(text=str(board.mines - flag_count))


#When a mine is clicked, sets all squares to show a mine and turn red indicating game over
def lose_game(board):
    for y in range(board.y):
        for x in range(board.x):
            buttons[x][y].config(text="  *  ")
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="red")


#When all non-mine buttons are clicked, all buttons are turned green indicating a win
def win_game(board):
    for y in range(board.y):
        for x in range(board.x):
            buttons[x][y]["state"] = "disabled"
            buttons[x][y].configure(bg="green")
            if board.squares[x][y].is_mine:
                buttons[x][y].config(text="  *  ")


#Function checks whether all non-mines have been clicked in order to end or continue the game
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


#Function to create the thread to manage timer and update the timer label every second 
def update_timer():
    global timer
    t = threading.Timer(1.0, update_timer)
    t.daemon = True
    t.start()
    timer+=1
    time_label.config(text=str(timer))


#Function to set up a new game
def new_game():
    global board
    global flag_count
    global timer
    board = Board()
    for i in range(board.y):
        for j in range(board.x): 
            buttons[j][i]["state"] = "normal"
            buttons[j][i].configure(bg="gray")
            buttons[j][i].config(text="      ")
    flag_count=0
    flag_label.config(text=str(board.mines))
    timer=0
    time_label.config(text=str(timer))


#Assign new game function to new game button
new_button.config(command=lambda : new_game())                

#Assign functions to each game button to check square when clicked
for i in range(board.y):
    for j in range(board.x):
        buttons[j][i].config(command=lambda i=i, j=j: check_square(j, i, board))
        buttons[j][i].bind("<Button-2>", right_click)
        buttons[j][i].bind("<Button-3>", right_click) 


#Create window
root.mainloop()

#Start timer
update_timer()        
