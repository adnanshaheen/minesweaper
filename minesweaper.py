from tkinter import *
import time
from tkinter.messagebox import *
import random

class Game:

    def __init__(self, master):

        self.frame = Frame(root, width = 910, bd = 8, relief = SUNKEN)
        self.frame.grid(row = 0, columnspan = 10)

        self.temp_lable = Label(self.frame, width = 37)
        self.temp_lable.grid(row = 0, column = 2)

        self.photo_new_game = PhotoImage(file = 'C:/temp/new_game_button.png')
        self.photo_lost_game = PhotoImage(file = 'C:/temp/lost.png')
        self.photo_won_game = PhotoImage(file = 'C:/temp/won.png')
        self.photo_flag = PhotoImage(file = 'C:/temp/flag.png')
        self.photo_mine = PhotoImage(file = 'C:/temp/mine.png')
        self.photo_plain = PhotoImage(file = 'C:/temp/tile_plain.gif')
        self.photo_clicked = PhotoImage(file = 'C:/temp/tile_clicked.gif')
        self.photo_1 = PhotoImage(file = 'C:/temp/tile_1.gif')
        self.photo_2 = PhotoImage(file = 'C:/temp/tile_2.gif')
        self.photo_3 = PhotoImage(file = 'C:/temp/tile_3.gif')
        self.photo_4 = PhotoImage(file = 'C:/temp/tile_4.gif')
        self.photo_5 = PhotoImage(file = 'C:/temp/tile_5.gif')
        self.photo_6 = PhotoImage(file = 'C:/temp/tile_6.gif')
        self.photo_7 = PhotoImage(file = 'C:/temp/tile_7.gif')
        self.photo_8 = PhotoImage(file = 'C:/temp/tile_8.gif')

        self.status_btn = Button(self.frame, image = self.photo_new_game, command = self.status_reset)
        self.status_btn.grid(row = 0, column = 1, columnspan = 2)

        self.btn_frame = Frame(root, bd = 8, relief = SUNKEN)
        self.btn_frame.grid(row = 1, columnspan = 10)

        self.total = 0
        self.lcount = 0
        self.rcount = 0
        self.first_click = True

        self.create_buttons(self.btn_frame)

    def create_buttons(self, parent):
        self.buttons = {}
        row = 1
        col = 0
        for i in range(0, 81):
            mine = 'safe'
            self.buttons[i] = [
                Button(parent, height = 1, width = 2, bg = '#adadad', border = 5),
                mine,
                row,
                col,
                0,
                0
            ]

            self.buttons[i][0].bind('<Button-1>', self.bind_left_click(i))
            self.buttons[i][0].bind('<Button-3>', self.bind_right_click(i))
            col += 1
            if col == 9:
                col = 0
                row += 1
            for k in self.buttons:
                self.buttons[k][0].grid(row = self.buttons[k][2], column = self.buttons[k][3])

        self.add_mines()

    def add_mines(self):
        while True:
            for pos in self.buttons:
                if self.total == 10:
                    return
                if random.uniform(0.0, 1.0) < 0.1 and self.buttons[pos][4] == 0 and self.total < 11:
                    self.buttons[pos][1] = 'danger'
                    self.buttons[pos][4] = 1
                    self.total += 1


    def bind_left_click(self, pos):
        return lambda Button: self.left_click(pos)

    def bind_right_click(self, pos):
        return lambda Button: self.right_click(pos)

    def left_click(self, pos):
        if self.buttons[pos][1] == 'danger':
            if self.first_click == True:
                self.buttons[pos][1] = 'safe'
                self.buttons[pos][4] = 0
                self.total -= 1
                self.add_mines()
            else:
                if self.buttons[pos][5] != 1:       # we are good, we already marked it is mine
                    self.buttons[pos][0].configure(bg = 'red')     # the image is gray, so part of button is gray
                    self.buttons[pos][0].configure(image = self.photo_mine)
                    self.buttons[pos][0].configure(state = DISABLED, height = 20, width = 18, relief = SUNKEN)
                    self.lost()

        if self.buttons[pos][1] == 'safe':
            if self.buttons[pos][5] != 2:
                self.buttons[pos][0].configure(state = 'disabled', relief = SUNKEN)
                self.lcount += 1
                self.buttons[pos][5] = 2
                self.nearby_mines(pos)
                self.nearby_safe(pos)
                if self.game_won():
                    self.won()

        self.first_click = False

    def right_click(self, pos):
        """ Right Click """
        if self.buttons[pos][5] == 0:
            self.buttons[pos][0].configure(image = self.photo_flag)
            self.buttons[pos][0].configure(state = DISABLED, height = 20, width = 18)
            self.buttons[pos][5] = 1
            if self.buttons[pos][1] == 'danger':
                self.rcount += 1
        elif self.buttons[pos][5] == 1:
            self.buttons[pos][0].configure(image = '')
            self.buttons[pos][0].configure(state = NORMAL, height = 1, width = 2)
            self.buttons[pos][5] = 0
            if self.buttons[pos][1] == 'danger':
                self.rcount -= 1

        self.first_click = False

    def nearby_safe(self, btn):
        next_pos = self.get_next_pos(btn)
        for i in next_pos:
            try:
                if self.buttons[i][1] == 'safe':
                    if self.buttons[i][5] == 2 or self.buttons[i][5] == 1:  # continue if user has right clicked
                        continue
                    else:
                        self.buttons[i][0].configure(state='disabled', relief=SUNKEN)
                        self.lcount += 1
                        self.buttons[i][5] = 2
                        if self.nearby_mines(i) == 0:
                            # even though list contain duplicate
                            # but we won't do anything so no problem
                            next_pos += self.get_next_pos(i)

            except KeyError:
                pass

    def nearby_mines(self, btn):
        near = 0
        next_pos = self.get_next_pos(btn)

        for pos in next_pos:
            try:
                if self.buttons[pos][1] == 'danger':
                    near += 1
            except KeyError:
                pass

        if near > 0:
            if near == 1:
                self.buttons[btn][0].configure(image = self.photo_1)
            elif near == 2:
                self.buttons[btn][0].configure(image = self.photo_2)
            elif near == 3:
                self.buttons[btn][0].configure(image = self.photo_3)
            elif near == 4:
                self.buttons[btn][0].configure(image = self.photo_4)
            elif near == 5:
                self.buttons[btn][0].configure(image = self.photo_5)
            elif near == 6:
                self.buttons[btn][0].configure(image = self.photo_6)
            elif near == 7:
                self.buttons[btn][0].configure(image = self.photo_7)
            elif near == 8:
                self.buttons[btn][0].configure(image = self.photo_8)

            self.buttons[btn][0].configure(height = 20, width = 18)
        else:
            return near

    def lost(self):
        for pos in self.buttons:
            if self.buttons[pos][1] == 'danger':
                self.buttons[pos][0].configure(image = self.photo_mine)
                self.buttons[pos][0].configure(state = DISABLED, height = 20, width = 18, relief = SUNKEN)


        self.status_btn.configure(image = self.photo_lost_game)

    def get_next_pos(self, btn):
        next_pos = []
        if btn == 0:
            next_pos = [btn + 1, btn + 9, btn + 10]
        elif btn == 8:
            next_pos = [btn - 1, btn + 8, btn + 9]
        elif btn == 72:
            next_pos = [btn - 9, btn - 8, btn + 1]
        elif btn == 80:
            next_pos = [btn - 10, btn - 9, btn - 1]
        elif btn < 8:
            next_pos = [btn - 1, btn + 1, btn + 8, btn + 9, btn + 10]
        elif btn % 9 == 0:
            next_pos = [btn - 9, btn - 8, btn + 1, btn + 9, btn + 10]
        elif (btn + 1) % 9 == 0:
            next_pos = [btn - 10, btn - 9, btn - 1, btn + 8, btn + 9]
        elif btn > 8 and btn < 72:
            next_pos = [btn - 10, btn - 9, btn - 8, btn - 1, btn + 1, btn + 8, btn + 9, btn + 10]
        elif btn > 72:
            next_pos = [btn - 10, btn - 9, btn - 8, btn - 1, btn + 1]

        return next_pos

    def won(self):
        self.status_btn.configure(image = self.photo_won_game)
        for pos in self.buttons:
            if self.buttons[pos][1] == 'danger':
                self.buttons[pos][0].configure(image = self.photo_flag)
                self.buttons[pos][0].configure(state = DISABLED, height = 20, width = 18)
                self.buttons[pos][5] = 1


    def status_reset(self):
        self.status_btn.configure(image = self.photo_new_game)

        for pos in self.buttons:
            self.buttons[pos][0].configure(bg = '#adadad')
            self.buttons[pos][0].configure(state = NORMAL, image = '', height = 1, width = 2, relief = RAISED)
            self.buttons[pos][1] = 'safe'
            self.buttons[pos][5] = 0

        self.lcount = 0
        self.rcount = 0
        self.total = 0
        self.add_mines()

    def game_won(self):
        return self.lcount == 71 or (self.lcount == 71 and self.rcount == 10)

    def quit(self):
        global root
        root.quit()


def main():
    global root
    root = Tk()
    root.title('MineSweaper')
    game = Game(root)
    root.resizable(width = False, height = False)          # Don't allow resizing
    root.mainloop()

if __name__ == '__main__':
    main()