import copy
import random
import sys  #to quit the application
import pygame
import numpy as np
#width and height of display
width=500
height=500

#background colour
bg_colour=(159,211,199)
rows=3
cols=3
square_size=width//rows
line_colour=(250, 255, 254)
line_width=12

#circle parameterss
circle_color=(224, 220, 88)
circle_width=15
radius=square_size//4
#cross parameters
cross_color=(66,66,66)
cross_width=20
offset=50

#setup
pygame.init()
screen=pygame.display.set_mode( (width, height) )
pygame.display.set_caption('TIC TAC TOE')
screen.fill(bg_colour)
#board
class Board:
    def __init__(self):
        self.squares = np.zeros((rows, cols))
        # self.mark_square(1,1,2)
        # print(self.squares)
        self.empty_squares=self.squares
        self.marked_squares=0
    def mark_square(self, row,col,player):
        self.squares[row][col]=player
        self.marked_squares+=1
    def empty_square(self,rows,cols):
        return self.squares[rows][cols]==0
    def is_full(self):
        return self.marked_squares==9
    def is_empty(self):
        return self.marked_squares==0
    def get_empty_squares(self):
        empty_squares=[]
        for row in range(rows):
            for col in range(cols):
                if self.empty_square(row,col):
                    empty_squares.append((row,col))
        return empty_squares

    def final_state(self,show=False):
        '''
        @:return 0 if draw
        @:return 1 if player 1 wins
        @:return 2 if player 2 wins
        '''
        #vertical wins
        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col]!=0:
                if show:
                    color=cross_color if self.squares[0][col]==2 else circle_color
                    initial_pos=(col*square_size+square_size//2,20)
                    final_pos=(col*square_size+square_size//2,height-20)
                    pygame.draw.line(screen,color,initial_pos,final_pos,cross_width)
                return self.squares[0][col]
        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color=cross_color if self.squares[row][0]==2 else circle_color
                    initial_pos=(20,row*square_size+square_size//2)
                    final_pos=(width-20,row*square_size+square_size//2)
                    pygame.draw.line(screen, color, initial_pos, final_pos,cross_width)
                return self.squares[row][0]
        #descending diagonal wins
        if self.squares[0][0]==self.squares[1][1]==self.squares[2,2]!=0:
            if show:
                color = cross_color if self.squares[1][1] == 2 else circle_color
                initial_pos = (20, 20)
                final_pos = (width - 20, height-20)
                pygame.draw.line(screen, color, initial_pos, final_pos, cross_width)
            return self.squares[1][1]   #common between both the diagonals
        # ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0, 2] != 0:
            if show:
                color = cross_color if self.squares[1][1] == 2 else circle_color
                initial_pos = (20, height-20)
                final_pos = (width-20,20)
                pygame.draw.line(screen, color, initial_pos, final_pos, cross_width)
            return self.squares[1][1]  # common between both the diagonals

        #incase draw returning 0
        return 0
class AI:
    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player
    def random_choice(self,board):
        empty_squares=board.get_empty_squares()
        index=random.randrange(0,len(empty_squares))
        return empty_squares[index] #returning rows and columns
    def minimax(self,board,maxmizing):
        #termianl case
        case=board.final_state()

        #player1 wins
        if case==1:
            return 1,None #eval,move
        #player 2 wins
        if case==2:
            return -1 ,None #as player 2 is ai and maximizing is false i.e ai is minimizing
        # a draw
        elif board.is_full():
            return 0,None
        if maxmizing:
            max_eval=-50
            best_move=None
            empty_squares=board.get_empty_squares()
            for (row, col) in empty_squares:
                temporary_board = copy.deepcopy(board)  # copying the board
                temporary_board.mark_square(row, col, 1)
                eval = self.minimax(temporary_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move
        elif not maxmizing:  #for ai minimizing
            min_eval=50 #any number minimizing +infinity
            best_move=None
            empty_squares=board.get_empty_squares()
            for (row,col) in empty_squares:
                temporary_board=copy.deepcopy(board) #copying the board
                temporary_board.mark_square(row,col,self.player)
                eval=self.minimax(temporary_board,True)[0]
                if eval < min_eval:
                    min_eval=eval
                    best_move=(row,col)
            return min_eval,best_move
    def eval(self,main_board):
        if self.level==0:
            #random choice
            eval='random'
            move=self.random_choice(main_board)
        else:
            #minimax algo choice
            eval,move=self.minimax(main_board,False)
        print(f'Ai has chose to mark the square in position {move} with an eval of {eval}')
        return move  # row column

class game:
    def __init__(self):
        self.board=Board()
        self.player=1 #1-human,2-ai
        self.lines()
        self.ai=AI()
        self.game_mode='ai' #or ai
        self.running=True

    def make_move(self,rows,cols):
        self.board.mark_square(rows, cols, self.player)
        self.draw_fig(rows, cols)
        self.next_turn()
        # pygame.time.delay(1000)


    def lines(self):
        screen.fill(bg_colour)
        #verical lines
        pygame.draw.line(screen,line_colour,(square_size,0),(square_size,height),line_width)
        pygame.draw.line(screen,line_colour,(width - square_size,0),(width-square_size,height),line_width)
        #horizontal line
        pygame.draw.line(screen,line_colour,(0,square_size),(width,square_size),line_width)
        pygame.draw.line(screen,line_colour,(0,height-square_size),(width,height-square_size),line_width)
    def draw_fig(self,rows,cols):
        if self.player==1:
            #drawing circle
            center=(cols*square_size + square_size//2,rows*square_size +square_size//2)
            pygame.draw.circle(screen,circle_color,center,radius,circle_width,)
        elif self.player==2:
            #drawing cross
            #descending line
            start_desc=(cols*square_size+offset,rows*square_size+offset)
            end_desc=(cols*square_size+square_size-offset,rows*square_size+square_size-offset)
            pygame.draw.line(screen,cross_color,start_desc,end_desc,cross_width)
            # ascending line
            start_asc = (cols * square_size + offset, rows * square_size + square_size- offset)
            end_asc = (cols * square_size + square_size - offset, rows * square_size+ offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)

    def next_turn(self):
        self.player=self.player % 2 +1

    def change_game_mode(self):
        if self.game_mode=='pvp':
            self.game_mode='ai'
        else:
            self.game_mode='pvp'
    def reset(self):
        self.__init__()
    def game_is_over(self):
        return self.board.final_state(show=True)!=0 or self.board.is_full()
def main():
    # game object
    game_obj = game()
    board = game_obj.board
    ai = game_obj.ai
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # g_key: changing the game mode
                if event.key == pygame.K_g:
                    game_obj.change_game_mode()
                # r-restart
                if event.key == pygame.K_r:
                    game_obj.reset()
                    board = game_obj.board
                    ai = game_obj.ai
                # 0-random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                # 1-minmax
                if event.key == pygame.K_1:
                    ai.level = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                pos = event.pos
                rows = pos[1] // square_size
                cols = pos[0] // square_size
                # print(rows,cols)

                if board.empty_square(rows, cols) and game_obj.running:
                    game_obj.make_move(rows, cols)
                    print(board.squares)
                    if game_obj.game_is_over():
                        game_obj.running = False

        if game_obj.game_mode == 'ai' and game_obj.player == ai.player and game_obj.running:
            # ai methods
            row, col = ai.eval(board)
            board.mark_square(row, col, game_obj.player)
            game_obj.draw_fig(row, col)
            game_obj.next_turn()
            print(board.squares)
            if game_obj.game_is_over():
                game_obj.running = False
        pygame.display.update()

main()
