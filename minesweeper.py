from tkinter import *
from classes import Board
import threading

#possible settings: easy, medium, and hard
settings = [{'x':10, 'y':10, 'mines':10}, {'x':16, 'y':16, 'mines':40}, {'x':16, 'y':30, 'mines':99}]

#Create initial board and global variables
board = Board()
flag_count=0
timer=0
game_on=True

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
mode=StringVar(control_frame, '0')
easy_radio = Radiobutton(control_frame, text="Easy", variable=mode, value='0')
med_radio = Radiobutton(control_frame, text="Medium", variable=mode, value='1')
hard_radio = Radiobutton(control_frame, text="Hard", variable=mode, value='2')
easy_radio.grid(row=1, column=0)
med_radio.grid(row=1, column=1)
hard_radio.grid(row=1, column=2)
control_frame.columnconfigure(0, weight=1)
control_frame.columnconfigure(1, weight=0)
control_frame.columnconfigure(2, weight=1)

#Function to set up 2D array of buttons and attach to the GUI 
def create_buttons(board):
    buttons = []
    for i in range(board.y):
            row=[]
            for j in range(board.x):
                row.append(Button(button_frame, background="gray", text="      ", disabledforeground="black", height=1, width=2))
                row[j].grid(row=j,column=i, sticky='ew')  
            buttons.append(row)
    return buttons
buttons = create_buttons(board)

#Logic for when a game square is pressed 
def check_square(x, y, board):
    if board.squares[y][x].is_clicked or board.squares[y][x].is_flagged:
        return
    board.squares[y][x].click()
    if board.squares[y][x].is_mine:
        lose_game(board)
        return
    elif board.squares[y][x].adjacent == 0:
        buttons[y][x].configure(bg="LightGrey")
        buttons[y][x]["state"] = "disabled"
        x_adj = [x-1, x, x+1]
        y_adj = [y-1, y, y+1]
        for i in y_adj:
            for j in x_adj:
                if (0<=i<=(board.y - 1) and 0<=j<=(board.x - 1) and not board.squares[i][j].is_clicked):
                    check_square(j, i, board)
    else:
        buttons[y][x].config(text="  " + str(board.squares[y][x].adjacent) + "  ")
        buttons[y][x]["state"] = "disabled"
        buttons[y][x].configure(bg="LightGrey")
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
    global game_on
    game_on=False
    for y in range(board.y):
        for x in range(board.x):
            buttons[y][x].config(text="  *  ")
            buttons[y][x]["state"] = "disabled"
            buttons[y][x].configure(bg="red")


#When all non-mine buttons are clicked, all buttons are turned green indicating a win
def win_game(board):
    global game_on
    game_on=False
    for y in range(board.y):
        for x in range(board.x):
            buttons[y][x]["state"] = "disabled"
            buttons[y][x].configure(bg="green")
            if board.squares[y][x].is_mine:
                buttons[y][x].config(text="  *  ")


#Function checks whether all non-mines have been clicked in order to end or continue the game
def check_state(board):
    total = (board.x*board.y)-board.mines
    count=0
    for y in range(board.y):
        for x in range(board.x):
            if board.squares[y][x].is_clicked:
                count+=1
    if count < total:
        return
    else:
        win_game(board)


#Function to create the thread to manage timer and update the timer label every second 
def update_timer():
    global timer
    global game_on
    t = threading.Timer(1.0, update_timer)
    t.daemon = True
    t.start()
    if game_on:
        timer+=1
    time_label.config(text=str(timer))


#Function to set up a new game
def radio_new_game():
    choice  = int(mode.get())
    global board
    global flag_count
    global timer
    global buttons
    global button_frame
    global game_on
    board = Board(settings[choice]['x'], settings[choice]['y'], settings[choice]['mines'])
    button_frame.destroy()
    button_frame = Frame(root)
    button_frame.pack( side = BOTTOM, fill='x', expand=True )
    buttons = create_buttons(board)
    buttons = assign_button_funcs(buttons)
    flag_count=0
    flag_label.config(text=str(board.mines))
    timer=0
    time_label.config(text=str(timer))
    game_on = True


#Assign functions to control buttons
new_button.config(command=radio_new_game)
easy_radio.config(command=radio_new_game)
med_radio.config(command=radio_new_game)
hard_radio.config(command=radio_new_game)                

#Assign functions to each game button to check square when clicked
def assign_button_funcs(buttons):
    global board
    for i in range(board.y):
        for j in range(board.x):
            buttons[i][j].config(command=lambda i=i, j=j: check_square(j, i, board))
            buttons[i][j].bind("<Button-2>", right_click)
            buttons[i][j].bind("<Button-3>", right_click)
    return buttons
buttons = assign_button_funcs(buttons)

#Start timer
update_timer()  

#Create window
root.mainloop()

      
