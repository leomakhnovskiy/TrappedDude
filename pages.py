from tkinter import *
from values import *
from PIL import Image, ImageTk
from random import randint
import json

def read_info_file(attribute):
    '''display a given piece of information from the info file'''

    info_file = open('info.json')
    info_content = json.load(info_file)
    info_file.close()
    return info_content[attribute]

def modify_info_file(attribute, new_data):
    '''change information from the info file given a variable to change and the new value'''

    info_file = open('info.json')
    info_content = json.load(info_file)
    info_file.close()

    info_content[attribute] = new_data

    with open('info.json', 'w') as new_file:
        json.dump(info_content, new_file)

def read_leaders_file(attribute):
    '''returns a value from leaders given an index'''

    leaders_file = open('leaders.json')
    leaders_content = json.load(leaders_file)
    leaders_file.close()
    return leaders_content[attribute]
    
    
class PageControl():
    def __init__(self, window):

        self.page_frames_dict = {}  # page dictionary

        # creates dictionary for all pages
        for page in (HomePage, LeaderboardPage, GamePage, SettingsPage, PausePage, EndPage, BossPage):
            page_name = page.__name__
            
            page_frame = page(window = window, control_object = self)
            page_frame.grid(row=0, column=0, sticky=NSEW)
            
            self.page_frames_dict[page_name] = page_frame

        self.page_frames_dict['HomePage'].lift()    # initially open the homepage

    def display_page(self, page_name):
        global read_info_file, modify_info_file

        self.page_frames_dict[page_name].lift() # display the page

        if page_name == 'GamePage':
            # unpause the game when game page is reopened
            paused = read_info_file('pause')
            if paused == 1:
                modify_info_file('pause', 0)

            # reset if new game started
            else:
                self.page_frames_dict[page_name].reset()
                
            # restart the game loop
            self.page_frames_dict[page_name].game_loop() 

        elif page_name == 'EndPage' or page_name == 'LeaderboardPage':
            self.page_frames_dict[page_name].update_page()

        elif page_name == 'PausePage':
            self.page_frames_dict[page_name].update_info()

        elif page_name == 'BossPage':
            self.page_frames_dict[page_name].update_info()
            self.page_frames_dict[page_name].page_loop()

class HomePage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.control_object = control_object

        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)
    
        # empty space
        emptyspace = Label(page_canvas, height=5, bg=COL2)
        emptyspace.grid(column=0, row=0)

        # Label containing game title
        game_title = Label(page_canvas,
                        text='Trapped Dude',
                        font=('Comic Sans MS', 100, 'bold'),
                        bg='black',
                        fg=COL1)
        game_title.grid(column=0, row=1)

        # empty space
        emptyspace2 = Label(page_canvas, height=3, bg=COL2)
        emptyspace2.grid(column=0, row=2)

        # Play button
        play_button = Button(page_canvas,
                            text='Play',
                            font=('SimSun', 40),
                            width=17,
                            pady=25,
                            bg=COL2,
                            relief=RIDGE,
                            activebackground=COL2,
                            fg=COL1,
                            command= lambda: control_object.display_page('GamePage'))
        play_button.grid(column=0, row=3)

        # empty space
        emptyspace3 = Label(page_canvas, font=('Arial', 1), height=1, bg=COL2)
        emptyspace3.grid(column=0, row=4)

        # Leaderboard button
        leaderboard_button = Button(page_canvas,
                                    text='Leaderboard',
                                    font=('SimSun', 40),
                                    width=17,
                                    bg=COL2,
                                    relief=RIDGE,
                                    activebackground=COL2,
                                    fg=COL1,
                                    command= lambda: control_object.display_page('LeaderboardPage'))
        leaderboard_button.grid(column=0, row=5)

        # empty space
        emptyspace4 = Label(page_canvas, font=('Arial', 1), height=1, bg=COL2)
        emptyspace4.grid(column=0, row=6)

        # Settings button
        settings_button = Button(page_canvas,
                                text='Settings',
                                font=('SimSun', 40),
                                width=17,
                                bg=COL2,
                                relief=RIDGE,
                                activebackground=COL2,
                                fg=COL1,
                                command= lambda: control_object.display_page('SettingsPage'))
        settings_button.grid(column=0, row=7)

        page_canvas.pack()
        window.update()


class EndPage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.control_object = control_object

        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)

        score = read_info_file('score')
        # score display text
        self.endpage_score = Label(page_canvas,
                        text=f'Final score = {score}',
                        font=('Comic Sans MS', 70, 'bold'),
                        bg='black',
                        fg=COL1,)
        self.endpage_score.grid(column=0, row=0, pady=20, columnspan=2)

        # entry for player to type name
        self.name_entry = Entry(page_canvas, font=('SimSun', 25))
        self.name_entry.grid(column=0, row=1, sticky='e')
        self.name_entry.insert(0, "Anonymous")

        # submit button
        self.submit_button = Button(page_canvas,
                            text='Submit',
                            font=('SimSun', 20),
                            bg=COL2,
                            relief=RIDGE,
                            activebackground=COL2,
                            fg=COL1,
                            command= self.update_leaderboard)
        self.submit_button.grid(column=1, row=1, sticky='w')

        # homepage button
        homepage_button = Button(page_canvas,
                            text='Homepage',
                            font=('SimSun', 40),
                            bg=COL2,
                            relief=RIDGE,
                            activebackground=COL2,
                            fg=COL1,
                            command= lambda: control_object.display_page('HomePage'))
        homepage_button.grid(column=0, row=2, pady=50, columnspan=2)
        
        page_canvas.pack()
        window.update()

    def update_page(self):
        '''Reads players new score and updates score display'''

        self.name_entry.delete(0, 'end')
        self.name_entry.insert(0, "Anonymous")  # reset name entry

        # update score display
        score = read_info_file('score')
        self.endpage_score.config(text=f'Final score = {score}')
    
    def update_leaderboard(self):
        '''updates the leaderboard based of the players score'''

        name = self.name_entry.get()
        score = read_info_file('score')

         # open leaders file
        leaders_file = open('leaders.json')
        leaders_content = json.load(leaders_file)
        leaders_file.close()

        # update leaderboard
        carry = [name, score]
        if carry[1] > leaders_content[0][1]:
            carry = leaders_content[0]
            leaders_content[0] = [name, score]

        if carry[1] > leaders_content[1][1]:
            temp = carry
            carry = leaders_content[1]
            leaders_content[1] = temp

        if carry[1] > leaders_content[2][1]:
            temp = carry
            carry = leaders_content[2]
            leaders_content[2] = temp

        if carry[1] > leaders_content[3][1]:
            temp = carry
            carry = leaders_content[3]
            leaders_content[3] = temp

        if carry[1] > leaders_content[4][1]:
            leaders_content[4] = carry

        # update leaders file
        with open('leaders.json', 'w') as file:
            json.dump(leaders_content, file)

        # open homepage after submission to prevent multiple submissions
        self.control_object.display_page('HomePage')


class LeaderboardPage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.control_object = control_object

        global read_leaders_file

        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)
        
        # back button
        back_button = Button(page_canvas,
                             text='Back',
                             font=('SimSun', 25),
                             width=11,
                             bg=COL2,
                             relief=RIDGE,
                             activebackground=COL2,
                             fg=COL1,
                             command= lambda: control_object.display_page('HomePage'))
        back_button.grid(column=0, row=0, sticky='nw', padx=5, pady=5)

        # 1st place text display
        first_name = read_leaders_file(0)[0]
        first_score = read_leaders_file(0)[1]
        self.rank1 = Label(page_canvas, text=f'1. {first_name}, {first_score}', bg=COL2, fg=COL1, width=60, height=2, font=('SimSun', 25))
        self.rank1.grid(column=0, row=1)

        # 2nd place text display
        second_name = read_leaders_file(1)[0]
        second_score = read_leaders_file(1)[1]
        self.rank2 = Label(page_canvas, text=f'2. {second_name}, {second_score}', bg=COL2, fg=COL1, width=50, height=2, font=('SimSun', 25))
        self.rank2.grid(column=0, row=2)

        # 3rd place text display
        third_name = read_leaders_file(2)[0]
        third_score = read_leaders_file(2)[1]
        self.rank3 = Label(page_canvas, text=f'3. {third_name}, {third_score}', bg=COL2, fg=COL1, width=50, height=2, font=('SimSun', 25))
        self.rank3.grid(column=0, row=3)

        # 4th place text display
        fourth_name = read_leaders_file(3)[0]
        fourth_score = read_leaders_file(3)[1]
        self.rank4 = Label(page_canvas, text=f'4. {fourth_name}, {fourth_score}', bg=COL2, fg=COL1, width=50, height=2, font=('SimSun', 25))
        self.rank4.grid(column=0, row=4)

        #5th place text display
        fifth_name = read_leaders_file(4)[0]
        fifth_score = read_leaders_file(4)[1]
        self.rank5 = Label(page_canvas, text=f'5. {fifth_name}, {fifth_score}', bg=COL2, fg=COL1, width=50, height=2, font=('SimSun', 25))
        self.rank5.grid(column=0, row=5)

        page_canvas.pack()
        window.update()

    def update_page(self):
        '''Reads leaders file and updates the page to display new top scores'''

        first_name = read_leaders_file(0)[0]
        first_score = read_leaders_file(0)[1]
        self.rank1.config(text=f'1. {first_name}, {first_score}')

        second_name = read_leaders_file(1)[0]
        second_score = read_leaders_file(1)[1]
        self.rank2.config(text=f'2. {second_name}, {second_score}')

        third_name = read_leaders_file(2)[0]
        third_score = read_leaders_file(2)[1]
        self.rank3.config(text=f'3. {third_name}, {third_score}')

        fourth_name = read_leaders_file(3)[0]
        fourth_score = read_leaders_file(3)[1]
        self.rank4.config(text=f'4. {fourth_name}, {fourth_score}')

        fifth_name = read_leaders_file(4)[0]
        fifth_score = read_leaders_file(4)[1]
        self.rank5.config(text=f'5. {fifth_name}, {fifth_score}')


class SettingsPage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.control_object = control_object
        
        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)
        
        # back button
        back_button = Button(page_canvas,
                             text='Back',
                             font=('SimSun', 25),
                             width=11,
                             bg=COL2,
                             relief=RIDGE,
                             activebackground=COL2,
                             fg=COL1,
                             command=self.back_pressed)
        back_button.grid(column=0, row=0, padx=5, pady=5, columnspan=2, sticky='nw')

        # up movement text
        self.up_move_label = Label(page_canvas, text='Up movement', bg=COL2, fg=COL1, width=35, height=2, font=('SimSun', 25))
        self.up_move_label.grid(column=0, row=1)
        # up movement input
        self.up_move_entry = Entry(page_canvas, font=('SimSun', 25))
        self.up_move_entry.grid(column=1, row=1)
        # down movement text
        self.down_move_label = Label(page_canvas, text='Down movement', bg=COL2, fg=COL1, width=35, height=2, font=('SimSun', 25))
        self.down_move_label.grid(column=0, row=2)
        # down movement input
        self.down_move_entry = Entry(page_canvas, font=('SimSun', 25))
        self.down_move_entry.grid(column=1, row=2)
        # left movement text
        self.left_move_label = Label(page_canvas, text='Left movement', bg=COL2, fg=COL1, width=35, height=2, font=('SimSun', 25))
        self.left_move_label.grid(column=0, row=3)
        # left movement input
        self.left_move_entry = Entry(page_canvas, font=('SimSun', 25))
        self.left_move_entry.grid(column=1, row=3)
        # right movement text
        self.right_move_label = Label(page_canvas, text='Right movement', bg=COL2, fg=COL1, width=35, height=2, font=('SimSun', 25))
        self.right_move_label.grid(column=0, row=4)
        # right movement input
        self.right_move_entry = Entry(page_canvas, font=('SimSun', 25))
        self.right_move_entry.grid(column=1, row=4)
        
        page_canvas.grid(column=0, row=0, sticky='nsew')        
        window.update()

    def back_pressed(self):
        '''update character movement keys when back is pressed, by grabbing text from input boxes'''
        
        modify_info_file('upkey', self.up_move_entry.get())
        modify_info_file('downkey', self.down_move_entry.get())
        modify_info_file('leftkey', self.left_move_entry.get())
        modify_info_file('rightkey', self.right_move_entry.get())

        self.control_object.display_page('HomePage')


class PausePage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.control_object = control_object

        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)

        # empty space
        emptyspace = Label(page_canvas, height=15, bg=COL2)
        emptyspace.grid(column=0, row=0)

        # play button
        play_button = Button(page_canvas,
                            text='Unpause',
                            font=('SimSun', 40),
                            bg=COL2,
                            relief=RIDGE,
                            activebackground=COL2,
                            fg=COL1,
                            width=20,
                            command= lambda: control_object.display_page('GamePage'))
        play_button.grid(column=0, row=1)

        # homepage button
        homepage_button = Button(page_canvas,
                            text='Homepage',
                            font=('SimSun', 40),
                            bg=COL2,
                            relief=RIDGE,
                            activebackground=COL2,
                            fg=COL1,
                            width=20,
                            command= lambda: self.control_object.display_page('HomePage'))
        homepage_button.grid(column=0, row=2, pady=10)

        page_canvas.pack()
        window.update()

    def update_info(self):
        '''sets the game to paused state'''

        modify_info_file('pause', 1)


class BossPage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.window = window
        self.control_object = control_object

        self.config(bg=COL2)    # set background

        # page canvas which will contain all elements
        page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)

        # create boss page photo
        bossphoto = Image.open('bossphoto.png')
        bossphoto = bossphoto.resize((WIDTH, HEIGHT))
        bossphoto = ImageTk.PhotoImage(bossphoto)
        window.bossphoto = bossphoto

        # display boss page photo
        self.displayed_bossphoto = page_canvas.create_image(0, 0, image=bossphoto, anchor=NW)
        
        page_canvas.pack()
        window.update()

    def update_info(self):
        '''sets the game to paused state'''

        modify_info_file('pause', 1)

    def key_pressed(self, event):
        '''opens game page when escape button is pressed again'''

        if event.keysym == 'Escape':
            self.control_object.display_page('GamePage')

    def page_loop(self):
        '''loop until escape is pressed again to exit boss page'''

        pause = read_info_file('pause')
        if pause == 0:
            return

        self.window.bind('<KeyPress>', self.key_pressed)

        self.after(10, self.page_loop)


class GamePage(Frame):
    def __init__(self, window, control_object):
        super().__init__(window)
        self.window = window
        self.control_object = control_object

        modify_info_file('pause', 0)    # initially dont pause

        # contains menu items at the top of the game screen - score/lives and pause button
        menu_canvas = Canvas(self, bg=COL2, highlightthickness=0)
        menu_canvas.place(relx=0, rely=0, relheight=0.1, relwidth=1)

        # display score text
        self.score_display = Label(menu_canvas, text=f'Score = 0', font=('Comic Sans MS', 36), bg=COL2, fg=COL1)
        self.score_display.place(relx=0.04, rely=0.17)

        # display lives text
        self.lives_display = Label(menu_canvas, text=f'Lives: 3', font=('Comic Sans MS', 36), bg=COL2, fg=COL1)
        self.lives_display.place(relx=0.43, rely=0.17)

        # display pause button
        pause_button = Button(menu_canvas,
                                    text='Pause',
                                    font=('Comic Sans MS', 25),
                                    bg=COL2,
                                    relief=RIDGE,
                                    activebackground=COL2,
                                    fg=COL1,
                                    command = lambda: self.control_object.display_page('PausePage'))
        pause_button.place(relx=0.88, relheight=1)
        
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               [1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1],
               [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 1],
               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # creating and resizing character image
        self.character = Image.open('character.png')
        self.character = self.character.resize((40, 36))
        self.character = ImageTk.PhotoImage(self.character)
        self.window.character = self.character

        # creating and resizing enemy image
        self.enemy = Image.open('enemy.png')
        self.enemy = self.enemy.resize((40, 36))
        self.enemy = ImageTk.PhotoImage(self.enemy)
        self.window.enemy = self.enemy
    
    def reset(self):
        '''resets the game page so a new game is ready to be played''' 

        modify_info_file('pause', 0)
        modify_info_file('score', 0)    # set score back to 0
        self.score_display.config(text='Score = 0')
        self.lives = 3  # set lives back to 3

        # new reset page canvas
        self.page_canvas = Canvas(self,
                         width=WIDTH,
                         height=HEIGHT,
                         bg=COL2,
                         highlightthickness=0)
        self.page_canvas.place(relx=0, rely=0.1, relheight=0.9, relwidth=1, anchor=NW)

        # places character back in start position
        self.displayed_character = self.page_canvas.create_image(40, 36, image=self.character, anchor=NW)
        
        self.blocks, self.coins = [], []
        #create a blocks/walls where the items in the map = 1 and a coin where item = 0    
        for row_index, row_item in enumerate(self.map):
            for col_index, item in enumerate(row_item):
                if item == 1:
                    block_x = col_index*40
                    block_y = row_index*36
                    block = self.page_canvas.create_rectangle(block_x, block_y, block_x+40, block_y+36, width=0, fill=COL1)
                    self.blocks.append(block)

                elif item == 0:
                    topleft_x = 15+col_index*40
                    topleft_y = 13+row_index*36
                    coin = self.page_canvas.create_rectangle(topleft_x+1, topleft_y+1, topleft_x+5, topleft_y+5, width=0, fill='yellow')
                    self.coins.append(coin)

        # game loop info
        self.direction = 0
        self.possibilities = [0, 0, 0, 0]
        self.keys_down = [0, 0, 0, 0]
        self.enemies = []
        self.enemies_direction = []

        self.spawn_enemies()    # spawn 3 initial enemies
        self.spawn_enemies()
        self.spawn_enemies()
        self.window.update()


    def game_loop(self):
        '''game loop which runs constantly while the game page is open''' 

        # stop the game loop if paused
        pause = read_info_file('pause')
        if pause == 1:
            return

        # stop the game loop and open end page if no lives left
        if self.lives == 0:
            self.control_object.display_page('EndPage')
            return

        # check key presses
        self.window.bind('<KeyPress>', self.key_press)
        self.window.bind('<KeyRelease>', self.key_release)

        self.update_movement_possibilities()
        self.check_direction_change()
        self.move_character()
        self.check_coin_collisions()
        self.move_enemies()

        self.window.update()
        self.after(10, self.game_loop)

    def move_enemies(self):
        '''generates a random direction for the enemy to move and detects collisions with player'''

        for enemy_index, enemy in enumerate(self.enemies):
            enemy_coords = self.page_canvas.bbox(enemy)
            movement_possibilities = [1, 1, 1, 1]

            # block collision detection
            for block in self.blocks:
                block_coords = self.page_canvas.bbox(block)

                # check if up movement possible
                if ((enemy_coords[0] >= block_coords[0]) and (enemy_coords[0] < block_coords[2])) or ((enemy_coords[2] > block_coords[0]) and (enemy_coords[2] <= block_coords[2])):
                    if enemy_coords[1] == block_coords[3]:
                        movement_possibilities[0] = 0

                #check if down movement possible
                if ((enemy_coords[0] >= block_coords[0]) and (enemy_coords[0] < block_coords[2])) or ((enemy_coords[2] > block_coords[0]) and (enemy_coords[2] <= block_coords[2])):
                    if enemy_coords[3] == block_coords[1]:
                        movement_possibilities[1] = 0

                #check if left movement possible
                if ((enemy_coords[1] >= block_coords[1]) and (enemy_coords[1] < block_coords[3])) or ((enemy_coords[3] <= block_coords[3]) and (enemy_coords[3] > block_coords[1])):
                    if enemy_coords[0] == block_coords[2]:
                        movement_possibilities[2] = 0

                #check if right movement possible
                if ((enemy_coords[1] >= block_coords[1]) and (enemy_coords[1] < block_coords[3])) or ((enemy_coords[3] <= block_coords[3]) and (enemy_coords[3] > block_coords[1])):
                    if enemy_coords[2] == block_coords[0]:
                        movement_possibilities[3] = 0

            # move enemy by choosing a random direction which it has the possibility to move
            possible_directions = []
            for i in range(len(movement_possibilities)):
                if movement_possibilities[i] == 1:
                    if i == 0:
                        possible_directions.append(1)
                    elif i == 1:
                        possible_directions.append(2)
                    elif i == 2:
                        possible_directions.append(3)
                    elif i == 3:
                        possible_directions.append(4)

            next_direction = possible_directions[randint(0, len(possible_directions)-1)]

            if (self.enemies_direction[enemy_index] == 1 and next_direction != 2) or (self.enemies_direction[enemy_index] == 2 and next_direction != 1) or (self.enemies_direction[enemy_index] == 3 and next_direction != 4) or (self.enemies_direction[enemy_index] == 4 and next_direction != 3) or self.enemies_direction[enemy_index] == 0:
                self.enemies_direction[enemy_index] = next_direction

            if self.enemies_direction[enemy_index] == 1 and movement_possibilities[0] == 1:
                self.page_canvas.move(enemy, 0, -2)

            elif self.enemies_direction[enemy_index] == 2 and movement_possibilities[1] == 1:
                self.page_canvas.move(enemy, 0, 2)

            elif self.enemies_direction[enemy_index] == 3 and movement_possibilities[2] == 1:
                self.page_canvas.move(enemy, -2, 0)

            elif self.enemies_direction[enemy_index] == 4 and movement_possibilities[3] == 1:
                self.page_canvas.move(enemy, 2, 0)

            
            char_coords = self.page_canvas.bbox(self.displayed_character)
            character_collision = False

            # character collision detection
            if self.direction == 1:
                if ((char_coords[0] >= enemy_coords[0]) and (char_coords[0] < enemy_coords[2])) or ((char_coords[2] > enemy_coords[0]) and (char_coords[2] <= enemy_coords[2])):
                    if (char_coords[1] < enemy_coords[3]) and (char_coords[3] > enemy_coords[3]):
                        character_collision = True

            elif self.direction == 2:
                if ((char_coords[0] >= enemy_coords[0]) and (char_coords[0] < enemy_coords[2])) or ((char_coords[2] > enemy_coords[0]) and (char_coords[2] <= enemy_coords[2])):
                    if (char_coords[3] > enemy_coords[1]) and (char_coords[1] < enemy_coords[3]):
                        character_collision = True

            elif self.direction == 3:
                if ((char_coords[1] >= enemy_coords[1]) and (char_coords[1] < enemy_coords[3])) or ((char_coords[3] <= enemy_coords[3]) and (char_coords[3] > enemy_coords[1])):
                    if (char_coords[0] < enemy_coords[2]) and (char_coords[2] > enemy_coords[2]):
                        character_collision = True

            elif self.direction == 4:
                if ((char_coords[1] >= enemy_coords[1]) and (char_coords[1] < enemy_coords[3])) or ((char_coords[3] <= enemy_coords[3]) and (char_coords[3] > enemy_coords[1])):
                    if (char_coords[2] > enemy_coords[0]) and (char_coords[0] < enemy_coords[2]):
                        character_collision = True

            # decrement lives and remove enemy if it collides with character
            if character_collision:
                self.lives -= 1
                self.lives_display.config(text=f'Lives: {self.lives}')
                self.page_canvas.delete(enemy)
                self.enemies.remove(enemy)

    def spawn_enemies(self):
        '''create an enemy and place it in the bottom right'''

        displayed_enemy = self.page_canvas.create_image(1280-80, 648-72, image=self.enemy, anchor=NW)
        self.enemies.append(displayed_enemy)
        self.enemies_direction.append(0)

    def check_coin_collisions(self):
        '''deletes coin and increments score when character collides with a coin'''

        char_coords = self.page_canvas.bbox(self.displayed_character)

        for coin in self.coins:
            coin_coords = self.page_canvas.bbox(coin)
            coin_collision = False

            if self.direction == 1:
                if (coin_coords[0] > char_coords[0]) and (coin_coords[2] < char_coords[2]):
                    if (char_coords[1] < coin_coords[3]) and (char_coords[3] > coin_coords[3]):
                        coin_collision = True

            elif self.direction == 2:
                if (coin_coords[0] > char_coords[0]) and (coin_coords[2] < char_coords[2]):
                    if (char_coords[3] > coin_coords[1]) and (char_coords[1] < coin_coords[1]):
                            coin_collision = True

            elif self.direction == 3:
                if (coin_coords[1] > char_coords[1]) and (coin_coords[3] < char_coords[3]):
                    if (char_coords[0] < coin_coords[2]) and (char_coords[2] > coin_coords[2]):
                            coin_collision = True

            elif self.direction == 4:
                if (coin_coords[1] > char_coords[1]) and (coin_coords[3] < char_coords[3]):
                    if (char_coords[2] > coin_coords[0]) and (char_coords[0] < coin_coords[0]):
                            coin_collision = True
            
            # if collision detected: increment score & delete coin
            if coin_collision:
                score = read_info_file('score')
                self.score_display.config(text=f'Score = {score}')
                self.page_canvas.delete(coin)
                self.coins.remove(coin)

                modify_info_file('score', score+1)

        # if no coins left: reset coins and spawn another enemy
        if len(self.coins) == 0:
            self.create_coins()
            self.spawn_enemies()

    def move_character(self):
        '''moves character based on which direction is specified and if its able to move in that direction'''

        speed = 4
        
        # move up
        if self.direction == 1 and self.possibilities[0] == 1:
            self.page_canvas.move(self.displayed_character, 0, -speed)

        # move down
        elif self.direction == 2 and self.possibilities[1] == 1:
            self.page_canvas.move(self.displayed_character, 0, speed)

        # move left
        elif self.direction == 3 and self.possibilities[2] == 1:
            self.page_canvas.move(self.displayed_character, -speed, 0)
        
        # move right
        elif self.direction == 4 and self.possibilities[3] == 1:
            self.page_canvas.move(self.displayed_character, speed, 0)

    def check_direction_change(self):
        '''change character direction if keydown and no blocks in the way'''

        if self.keys_down[0] == 1 and self.possibilities[0] == 1:
            self.direction = 1

        if self.keys_down[1] == 1 and self.possibilities[1] == 1:
            self.direction = 2

        if self.keys_down[2] == 1 and self.possibilities[2] == 1:
            self.direction = 3

        if self.keys_down[3] == 1 and self.possibilities[3] == 1:
            self.direction = 4

    def update_movement_possibilities(self):
        '''check which directions the character is able to move in'''

        self.possibilities = [1, 1, 1, 1]
        char_coords = self.page_canvas.bbox(self.displayed_character)

        for block in self.blocks:
            block_coords = self.page_canvas.bbox(block)

            # check if up movement possible
            if ((char_coords[0] >= block_coords[0]) and (char_coords[0] < block_coords[2])) or ((char_coords[2] > block_coords[0]) and (char_coords[2] <= block_coords[2])):
                if char_coords[1] == block_coords[3]:
                    self.possibilities[0] = 0

            #check if down movement possible
            if ((char_coords[0] >= block_coords[0]) and (char_coords[0] < block_coords[2])) or ((char_coords[2] > block_coords[0]) and (char_coords[2] <= block_coords[2])):
                if char_coords[3] == block_coords[1]:
                    self.possibilities[1] = 0

            #check if left movement possible
            if ((char_coords[1] >= block_coords[1]) and (char_coords[1] < block_coords[3])) or ((char_coords[3] <= block_coords[3]) and (char_coords[3] > block_coords[1])):
                if char_coords[0] == block_coords[2]:
                    self.possibilities[2] = 0

            #check if right movement possible
            if ((char_coords[1] >= block_coords[1]) and (char_coords[1] < block_coords[3])) or ((char_coords[3] <= block_coords[3]) and (char_coords[3] > block_coords[1])):
                if char_coords[2] == block_coords[0]:
                    self.possibilities[3] = 0

    def create_coins(self):
        '''creates a new set of coin. called when the previous set has been fully collected'''

        for row_index, row_item in enumerate(self.map):
            for col_index, item in enumerate(row_item):
                if item == 0:
                    topleft_x = 15+col_index*40
                    topleft_y = 13+row_index*36
                    coin = self.page_canvas.create_rectangle(topleft_x+1, topleft_y+1, topleft_x+5, topleft_y+5, width=0, fill='yellow')
                    self.coins.append(coin)


    def key_press(self, event):
        '''detects keypresses'''

        if event.keysym == read_info_file('upkey'):
            self.keys_down[0] = 1
        if event.keysym == read_info_file('downkey'):
            self.keys_down[1] = 1
        if event.keysym == read_info_file('leftkey'):
            self.keys_down[2] = 1
        if event.keysym == read_info_file('rightkey'):
            self.keys_down[3] = 1

        if event.keysym == 'Escape':
            self.control_object.display_page('BossPage')

    def key_release(self, event):
        '''detects key releases'''

        if event.keysym == read_info_file('upkey'):
            self.keys_down[0] = 0
        if event.keysym == read_info_file('downkey'):
            self.keys_down[1] = 0
        if event.keysym == read_info_file('leftkey'):
            self.keys_down[2] = 0
        if event.keysym == read_info_file('rightkey'):
            self.keys_down[3] = 0
