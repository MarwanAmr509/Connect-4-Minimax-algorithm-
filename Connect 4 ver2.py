import numpy as np
import math
import random
import pygame
import sys
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
ROW = 6
COL= 7
ROW_HALF = math.ceil(ROW/2)
COL_HALF = math.ceil(COL/2)
def create_board():
    board = np.zeros((ROW,COL))
    return board
#selection is always a column
def drop_piece(board,row,selection,piece):
    board[row][selection] = piece


def is_valid_col(board,selection):
    return board[ROW-1][selection] == 0
def get_valid_col(board):
    valid_col=[]
    for c in range(COL):
        if is_valid_col(board,c):
            valid_col.append(c)
    return valid_col
        
    
        
def get_next_open_row(board,selection):
    for r in range(ROW):
        if board[r][selection]==0:
            return r
        
def print_board(board):
    print(np.flip(board,0)) #0 means flip it over the x-axis

def score_calc(line,piece):
    score = 0
    opp_piece = 1
    if piece == 1:
        opp_piece = 2
    if line.count(piece)==4:
        score = int(score + 100)
    elif line.count(piece) == 3 and line.count(0)==1:
        score = int(score + 10)
    elif line.count(piece)== 2 and line.count(0)==2:
        score = int(score +5) 

    if line.count(opp_piece) == 3 and line.count(opp_piece)==1:
        score = score - 9
    elif line.count(opp_piece) == 2 and line.count(opp_piece)==2:
        score = score - 3
    return score
def score_position(board,piece):
    score = 0
    #horizontal
    for r in range(ROW):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COL_HALF):
            line = row_array[c:c+4]
            score += score_calc(line,piece)
    #vertical
    for c in range(COL):
        col_array =  [int(i) for i in list(board[:,c])]
        for r in range(ROW_HALF):
            line = col_array[r:r+4]
            score += score_calc(line,piece)
    #DIAGONALLY POSITIVE
    for r in range(ROW_HALF):
        for c in range(COL_HALF):
            line = [board[r+i][c+i] for i in range(4)]
            score += score_calc(line,piece)
    #DIAGONALLY NEGATIVE
    for r in range(ROW-1,ROW_HALF-1,-1):
        for c in range(COL-1,COL_HALF-2,-1):
            line = [board[r-i][c-i] for i in range(4)]
            score += score_calc(line,piece)
    for r in range(ROW_HALF):
        for c in range(COL_HALF):
            line = [board[r+3-i][c+i]for i in range(4)]
            score += score_calc(line,piece)
    return score


def is_terminal_node(board):
    return winning_move(board,1) or winning_move(board,2) or len(get_valid_col(board))==0
def miniMax(board,depth,alpha,beta,maximizing):
    valid_col = get_valid_col(board)
    terminal_node = is_terminal_node(board)
    if depth == 0  or terminal_node:
        if terminal_node:
            if winning_move(board,2):
                return (None,10000000000)
            elif winning_move(board,1):
                return (None,-1000000000)
            else:
                return (None,0)
        else:   #depth is zero
            return (None,score_position(board,2))
    if maximizing: # maximizing player
        value = -math.inf
        column = random.choice(valid_col)
        for col in valid_col:
            row = get_next_open_row(board,col)
            board_copy = board.copy()
            drop_piece(board_copy,row,col,2)
            new_score = miniMax(board_copy,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha,value)
            if beta <= alpha:
                break
        return column,value
    else: #minimizing player
        value = math.inf
        column = random.choice(valid_col)
        for col in valid_col:
            row = get_next_open_row(board,col)
            board_copy = board.copy()
            drop_piece(board_copy,row,col,1)
            new_score = miniMax(board_copy,depth-1,alpha,beta,True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta,value)
            if beta <= alpha:
                break
        return column,value
    


            
def best_move(board,piece):
    valid_col = get_valid_col(board)
    best_score = -1000
    best_col = random.choice(valid_col)
    for c in valid_col:
        row = get_next_open_row(board,c)
        temp_board = board.copy()
        drop_piece(temp_board,row,c,piece)
        score = score_position(temp_board,piece)
        if score > best_score:
            best_score = int(score)
            best_col = c
    return best_col
def winning_move(board,piece):
    
    #checking horizontal locations
    for c in range(COL_HALF):
        for r in range(ROW):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True
    #checking vertical locations
    for c in range(COL):
        for r in range(ROW_HALF):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    #checking for positive diagonal locations
    for c in range(COL_HALF):
        for r in range(ROW_HALF):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True
    
    #checking fo negative diagonal locaiotns
    for c in range(COL_HALF):
        for r in range(3,ROW):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True


def draw_board(board):
    for c in range(COL):
        for r in range(ROW):
            pygame.draw.rect(screen,BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,BLACK,(c*SQUARE_SIZE+SQUARE_SIZE/2,r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2),RADIUS)
    pygame.display.update()
    for c in range(COL):
        for r in range(ROW):
            if board[r][c] == 1:
                pygame.draw.circle(screen,RED,(c*SQUARE_SIZE+SQUARE_SIZE/2,height-(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen,YELLOW,(c*SQUARE_SIZE+SQUARE_SIZE/2,height-(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIUS)
    pygame.display.update()
board =  create_board()
game_over = False
turn = random.randint(0,1)
#interface stuff
pygame.init()
SQUARE_SIZE = 100
width = COL*SQUARE_SIZE
height = (ROW+1)*SQUARE_SIZE
size = (width,height)
RADIUS = int(SQUARE_SIZE/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.set_caption("Connect 4")
pygame.display.update()
font = pygame.font.SysFont("monospace",50)
#interface stuff done

while not game_over:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
            posx = event.pos[0]
            if turn%2 == 0 and not game_over:
                pygame.draw.circle(screen,RED,(posx,SQUARE_SIZE/2),RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen,BLACK,(0,0,width,SQUARE_SIZE))
            #Player 1 input--piece for player 1 is 1
            if turn%2 == 0:
                    posx = event.pos[0]
                    selection =  math.floor(posx/SQUARE_SIZE)
                    if is_valid_col(board,selection):
                        row = get_next_open_row(board,selection)
                        drop_piece(board,row,selection,1)
                        if winning_move(board,1):
                            text =  font.render("PLAYER 1 WINS!!!!",1,RED)
                            screen.blit(text,(width/2-SQUARE_SIZE*2.5,SQUARE_SIZE/2-SQUARE_SIZE/4))
                            print("PLAYER 1 WINS!!!!")
                            game_over=True
                    turn += 1
                    print_board(board)
                    draw_board(board)

    if turn%2 == 1 and not game_over:
        #selection = best_move(board,2)
        selection,minimax_score = miniMax(board,4,-math.inf,math.inf,True)
        if is_valid_col(board,selection):
            #pygame.time.wait(1000) # if you want to add realistic part
            row = get_next_open_row(board,selection)
            drop_piece(board,row,selection,2)
            
            if winning_move(board,2):
                text =  font.render("PLAYER 2 WINS!!!!",1,YELLOW)
                screen.blit(text,(width/2-SQUARE_SIZE*2.5,SQUARE_SIZE/2-SQUARE_SIZE/4))
                print("PLAYER 2 WINS!!!!")
                game_over=True
                


            print_board(board)
            draw_board(board)
            turn += 1

   

  


                
