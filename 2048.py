import pygame
import random

pygame.init()

# COLORS AND FONTS
BG1_COLOR = (207 , 193, 178)
BG2_COLOR = (250, 248 , 238)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TITLE_COLOR = (119,110,101)
SCORE_BG_COLOR = (187,173,160)
SCORE_TEXT_COLOR = (238,228,218)
#FONT = pygame.font.SysFont("calibri", 30)
EMPTY_CELL_COLOR = (194,179,169)
GRID_COLOR = (163,148,137)
CELL_COLORS = {
    0: (194,179,169),
    2: (238,228,218), 
    4: (238,225,201), 
    8: (245,182,130), 
    16: (242,148,70), 
    32: (255,119,92), 
    64: (230,76,46), 
    128: (237,226,145), 
    256: (252,225,48), 
    512: (255,219,74), 
    1024: (240,185,34), 
    2048: (250,215,77)
}
CELL_NUMBER_COLORS = {
    2: (105,92,87),
    4: (105,92,87),
    8: (255, 255, 255),
    16: (255, 255, 255),
    32: (255, 255, 255),
    64: (255, 255, 255),
    128: (255, 255, 255),
    256: (255, 255, 255),
    512: (255, 255, 255),
    1024: (255, 255, 255),
    2048: (255, 255, 255)
}

# FONTS
TITLE_FONT = pygame.font.SysFont("roboto", 100, bold=True)
SCORE_TEXT_FONT = pygame.font.SysFont("roboto", 15, bold=True)
SCORE_NUMBER_FONT = pygame.font.SysFont("roboto", 30, bold=True)
CELL_NUMBER_FONT = "roboto"
CELL_NUMBER_SIZE = {
    2: 50,
    4: 50,
    8: 50,
    16: 50,
    32: 50,
    64: 50,
    128: 45,
    256: 45,
    512: 45,
    1024: 40,
    2048: 40,
}

# CONFIG
WIDTH = 600 # 768
HEIGHT = 800 # 1024
BORDER_WIDTH = 15 # 20
SQR_SZ = 123.75 # 157
BOARD_Y_POS = (HEIGHT-BORDER_WIDTH-(WIDTH-2*BORDER_WIDTH))
DELAY = 200
FPS = 60


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("2048")
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.new_game()

    # RESET GAME
    def new_game(self):
        self.create_board()
        self.score = 0
        self.move_time = pygame.time.get_ticks()
        self.spawn_new_numbers()
        self.spawn_new_numbers()
        self.update_board_list()
        self.loop()

    # MAIN GAME LOOP
    def loop(self):
        while True:
            self.clock.tick(FPS)
            self.check_events()
            self.handle_score()
            self.draw_window()

    # CREATING INITIAL BOARD DICT AT NEW GAME
    def create_board(self):
        self.board_dict = {
            0:0, 1:0, 2:0, 3:0, 
            4:0, 5:0, 6:0, 7:0, 
            8:0, 9:0, 10:0, 11:0, 
            12:0, 13:0, 14:0, 15:0
            }
    
    def update_board_list(self):
        self.board_list = [
            [self.board_dict[0], self.board_dict[1], self.board_dict[2], self.board_dict[3]],
            [self.board_dict[4], self.board_dict[5], self.board_dict[6], self.board_dict[7]],
            [self.board_dict[8], self.board_dict[9], self.board_dict[10], self.board_dict[11]],
            [self.board_dict[12], self.board_dict[13], self.board_dict[14], self.board_dict[15]]
        ]

    # GET PYGAME EVENTS QUIT AND PLATFORM INTERVAL
    def check_events(self):
        self.keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.new_game()
                if event.key == pygame.K_SPACE:
                    self.spawn_new_numbers()
                if event.key == pygame.K_UP:
                    self.handle_up_movement()
                if event.key == pygame.K_DOWN:
                    self.handle_down_movement()
                if event.key == pygame.K_LEFT:
                    self.handle_left_movement()
                if event.key == pygame.K_RIGHT:
                    self.handle_right_movement()

    # CREATING DICTIONARY WITH 0-15 INDEX AND A PYGAME RECT FOR EACH SQUARE
    def create_rect_squares(self):
        self.square_list = []
        self.square_dict = {}
        self.square_key = 0
        for i in range(0, 4):
            for j in range(0, 4):
                square = pygame.Rect(2*BORDER_WIDTH+j*(BORDER_WIDTH+SQR_SZ), BOARD_Y_POS+BORDER_WIDTH+i*(BORDER_WIDTH+SQR_SZ), SQR_SZ, SQR_SZ)
                self.square_list.append(square)
                self.square_dict[self.square_key] = square
                self.square_key += 1

    # CHECK FOR EMPTY CELLS AND FILL ONE WITH EITHER 2 OR 4
    def spawn_new_numbers(self):
        pygame.time.wait(DELAY)
        empty_cell_list = []
        for i in self.board_dict:
            if self.board_dict[i] == 0:
                empty_cell_list.append(i) # GETS A LIST OF DICT KEYS FOR ALL EMPTY CELLS
        if empty_cell_list:
            new_cell = random.choice(empty_cell_list)
            self.board_dict[new_cell] = random.choice([2, 2, 2, 2, 4, 4, 4]) # FILLS THE CHOSEN CELL WITH EITHER 2 OR 4

    def handle_adding(self, i, j):
        if self.board_dict[i] == self.board_dict[j]:    # SAME NUMBERS, ADDING
            self.board_dict[j] = self.board_dict[j]*2
            self.board_dict[i] = 0

    # MOVING CELLS UP AND ADDING THEM TOGETHER
    def handle_up_movement(self):
        control_list = self.board_list.copy()   # MAKING COPY TO SEE IF CELLS MOVED LATER
        for i in self.board_dict:
            h = i + 4   # BELOW NEIGHBOUR
            j = i - 4   # ABOVE NEIGHBOUR
            k = i - 8   # TWO ROWS ABOVE NEIGHBOUR
            try:
                if self.board_dict[i] == 0:
                    self.board_dict[i] = self.board_dict[h]
                    self.board_dict[h] = 0
                    if self.board_dict[j] ==0:
                        self.board_dict[j] = self.board_dict[i]
                        self.board_dict[i] = 0
                        if self.board_dict[k] ==0:
                            self.board_dict[k] = self.board_dict[j]
                            self.board_dict[j] = 0
                        else:
                            self.handle_adding(j, k)
                            continue
                    else:
                        self.handle_adding(i, j)
                        continue
                else:
                    self.handle_adding(h, i)
                    continue
            except KeyError:
                continue
        # ONCE ALL CELLS HAVE BEEN MOVED, SPAWN NEW NUMBERS
        self.update_board_list()
        if control_list != self.board_list:
            self.draw_window()
            self.spawn_new_numbers()

    # MOVING CELLS DOWN AND ADDING THEM TOGETHER
    def handle_down_movement(self):
        control_list = self.board_list.copy()   # MAKING COPY TO SEE IF CELLS MOVED LATER
        for i in reversed(self.board_dict):
            g = i + 8   # TWO ROWS BELOW NEIGHBOUR
            h = i + 4   # BELOW NEIGHBOUR
            j = i - 4   # ABOVE NEIGHBOUR
            try:
                if self.board_dict[i] == 0:
                    self.board_dict[i] = self.board_dict[j]
                    self.board_dict[j] = 0
                    if self.board_dict[h] ==0:
                        self.board_dict[h] = self.board_dict[i]
                        self.board_dict[i] = 0
                        if self.board_dict[g] ==0:
                            self.board_dict[g] = self.board_dict[h]
                            self.board_dict[h] = 0
                        else:
                            self.handle_adding(h, g)
                            continue
                    else:
                        self.handle_adding(i, h)
                        continue
                else:
                    self.handle_adding(j, i)
                    continue
            except KeyError:
                continue
        # ONCE ALL CELLS HAVE BEEN MOVED, SPAWN NEW NUMBERS
        self.update_board_list()
        if control_list != self.board_list:
            self.draw_window()
            self.spawn_new_numbers()

    # MOVING CELLS LEFT AND ADDING THEM TOGETHER
    def handle_left_movement(self):
        control_list = self.board_list.copy()   # MAKING COPY TO SEE IF CELLS MOVED LATER
        for i in [0, 4, 8, 12]:
            control = self.board_dict[i]
            self.handle_adding(i+1, i)
            if self.board_dict[i+1] == 0 and self.board_dict[i+2] == 0 and self.board_dict[i+3] == control:
                self.handle_adding(i+3, i)
            if self.board_dict[i+1] == 0 and self.board_dict[i+2] == control:
                self.handle_adding(i+2, i)
            if (self.board_dict[i+1] == 0 and self.board_dict[i+2] == 0) and self.board_dict[i+3] == control:
                self.handle_adding(i+3, i)
            elif self.board_dict[i+1] == self.board_dict[i+2]:
                self.handle_adding(i+2, i+1)
            elif self.board_dict[i+2] == 0 and self.board_dict[i+1] == self.board_dict[i+3]:
                self.handle_adding(i+3, i+1)
            elif self.board_dict[i+2] == self.board_dict[i+3]:
                self.handle_adding(i+3, i+2)
            for x in range(3):
                if self.board_dict[i+2] == 0:
                    self.board_dict[i+2] = self.board_dict[i+3]
                    self.board_dict[i+3] = 0
                if self.board_dict[i+1] == 0:
                    self.board_dict[i+1] = self.board_dict[i+2]
                    self.board_dict[i+2] = 0
                if self.board_dict[i] == 0:
                    self.board_dict[i] = self.board_dict[i+1]
                    self.board_dict[i+1] = 0
        # ONCE ALL CELLS HAVE BEEN MOVED, SPAWN NEW NUMBERS
        self.update_board_list()
        if control_list != self.board_list:
            self.draw_window()
            self.spawn_new_numbers()

    # MOVING CELLS RIGHT AND ADDING THEM TOGETHER
    def handle_right_movement(self):
        control_list = self.board_list.copy()   # MAKING COPY TO SEE IF CELLS MOVED LATER
        for i in [3, 7, 11, 15]:
            control = self.board_dict[i]
            self.handle_adding(i-1, i)
            if self.board_dict[i-1] == 0 and self.board_dict[i-2] == 0 and self.board_dict[i-3] == control:
                self.handle_adding(i-3, i)
            if self.board_dict[i-1] == 0 and self.board_dict[i-2] == control:
                self.handle_adding(i-2, i)
            if (self.board_dict[i-1] == 0 and self.board_dict[i-2] == 0) and self.board_dict[i-3] == control:
                self.handle_adding(i-3, i)
            elif self.board_dict[i-1] == self.board_dict[i-2]:
                self.handle_adding(i-2, i-1)
            elif self.board_dict[i-2] == 0 and self.board_dict[i-1] == self.board_dict[i-3]:
                self.handle_adding(i-3, i-1)
            elif self.board_dict[i-2] == self.board_dict[i-3]:
                self.handle_adding(i-3, i-2)
            for x in range(3):
                if self.board_dict[i-2] == 0:
                    self.board_dict[i-2] = self.board_dict[i-3]
                    self.board_dict[i-3] = 0
                if self.board_dict[i-1] == 0:
                    self.board_dict[i-1] = self.board_dict[i-2]
                    self.board_dict[i-2] = 0
                if self.board_dict[i] == 0:
                    self.board_dict[i] = self.board_dict[i-1]
                    self.board_dict[i-1] = 0
        # ONCE ALL CELLS HAVE BEEN MOVED, SPAWN NEW NUMBERS
        self.update_board_list()
        if control_list != self.board_list:
            self.draw_window()
            self.spawn_new_numbers()

    # CALCULATING SELF.SCORE
    def handle_score(self):
        self.score = 0
        for i in self.board_dict:
            self.score += self.board_dict[i]

    # DRAWING SQUARES WITH CORRECT NUMBERS AND COLORS USING SELF.SQUARE_DICT
    def draw_squares(self):
        # SQUARES
        self.create_rect_squares()
        for i in self.square_dict:
            #sqr_color = CELL_COLORS[i]
            cell_number = self.board_dict[i]
            cell_color = CELL_COLORS[cell_number]
            pygame.draw.rect(self.win, cell_color, self.square_dict[i], width=0, border_radius=20)
        # NUMBERS
        self.update_board_list()
        for i in range(0, 4):       # I = ROW
            for j in range(0 ,4):   # J = COL
                cell_number = self.board_list[i][j]
                if cell_number == 0:
                    continue
                number_font = pygame.font.SysFont(CELL_NUMBER_FONT, CELL_NUMBER_SIZE[cell_number], bold=True)
                cell_number_text = number_font.render(str(cell_number), 1, CELL_NUMBER_COLORS[cell_number])
                x = 2*BORDER_WIDTH+j*(BORDER_WIDTH+SQR_SZ) + (SQR_SZ//2-cell_number_text.get_width()//2)
                y = BOARD_Y_POS+BORDER_WIDTH+i*(BORDER_WIDTH+SQR_SZ) + (SQR_SZ//2-cell_number_text.get_height()//2)
                self.win.blit(cell_number_text, (x, y))


    def draw_rest(self):
        # TITLE
        title_text = TITLE_FONT.render("2048", 1, TITLE_COLOR)
        self.win.blit(title_text, (BORDER_WIDTH, 107.5-(title_text.get_height()//2)))
        # SCORE
        score_bg_width = 120
        score_bg_height = title_text.get_height()*0.7
        score_bg = pygame.Rect(WIDTH-(BORDER_WIDTH+120), 107.5-((score_bg_height)//2), 120, score_bg_height)
        pygame.draw.rect(self.win, SCORE_BG_COLOR, score_bg, width=0, border_radius=5)
        score_text = SCORE_TEXT_FONT.render("SCORE", 1, SCORE_TEXT_COLOR)
        self.win.blit(score_text, (WIDTH-(BORDER_WIDTH+120)+((score_bg_width-score_text.get_width())//2), 107.5-((score_bg_height)//2)+10))
        score_number_text = SCORE_NUMBER_FONT.render(str(self.score), 1, WHITE)
        self.win.blit(score_number_text, (WIDTH-(BORDER_WIDTH+120)+((score_bg_width-score_number_text.get_width())//2), 100))

    # DRAW EVERYTHING ON SCREEN, UPDATE SCREEN
    def draw_window(self):
        self.win.fill(BG2_COLOR)
        self.gridborder = pygame.Rect(BORDER_WIDTH, BOARD_Y_POS, WIDTH-2*BORDER_WIDTH, WIDTH-2*BORDER_WIDTH)
        pygame.draw.rect(self.win, GRID_COLOR, self.gridborder, width=0, border_radius=20)
        self.draw_squares()
        self.draw_rest()
        pygame.display.flip()


if __name__ == "__main__":
    Game()
