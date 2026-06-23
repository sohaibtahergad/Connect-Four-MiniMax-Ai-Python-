import pygame
import time      
import sys

ROWS = 6       
COLS = 7        

EMPTY = 0      
HUMAN = 1    
AI = 2        

DEPTH = 4

totalcount = 0
totaltime = 0
board = []    

for r in range(ROWS):   
    row = []  

    for c in range(COLS):   
        row.append(EMPTY)
       

    board.append(row)  


nodes = 0  
tm = 0
val = 0
game_over = False  


# =========================
# Board + Moves
# =========================


def is_valid_move(col):
    return board[0][col] == EMPTY


def drop_disc(col, player):    
    for r in range(ROWS - 1, -1, -1):  
        if board[r][col] == EMPTY:    
            board[r][col] = player    
            return r    


def undo_move(col):
    for r in range(ROWS): 
        if board[r][col] != EMPTY:  
            board[r][col] = EMPTY
            return


def is_full():   
    for c in range(COLS): 
        if is_valid_move(c):  
            return False
    return True


# =========================
# Win Detection
# =========================

def check_win(player):
    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
                return True

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
                return True

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
                return True

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
                return True

    return False


# =========================
# Heuristic + Nodes
# =========================

def score_four(a, b, c, d):
    group = [a, b, c, d]

    ai_count = group.count(AI)
    human_count = group.count(HUMAN)
    empty_count = group.count(EMPTY)

    if ai_count == 4:
        return 100
    if ai_count == 3 and empty_count == 1:
        return 5
    if ai_count == 2 and empty_count == 2:
        return 2
    if human_count == 3 and empty_count == 1:
        return -4

    return 0


def score_board():
    score = 0

    # Center column
    for r in range(ROWS):
        if board[r][3] == AI:
            score += 3

    # Horizontal
    for r in range(ROWS):
        for c in range(COLS - 3):
            score += score_four(board[r][c], board[r][c+1], board[r][c+2], board[r][c+3])

    # Vertical
    for r in range(ROWS - 3):
        for c in range(COLS):
            score += score_four(board[r][c], board[r+1][c], board[r+2][c], board[r+3][c])

    # Diagonal \
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            score += score_four(board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3])

    # Diagonal /
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            score += score_four(board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3])

    return score


# =========================
# Minimax
# =========================

def minimax(depth,alpha, beta, ai_turn):
    global nodes
    nodes += 1

    if check_win(AI):
        return 100000
    if check_win(HUMAN):
        return -100000
    if is_full():
        return 0
    if depth == 0:
        return score_board()

    if ai_turn:
        best = -1000000

        for c in range(COLS):
            if is_valid_move(c):
                drop_disc(c, AI)
                score = minimax(depth - 1,alpha, beta, False)
                undo_move(c)

                if score > best:
                    best = score
                alpha = max(alpha, score)
                if alpha >= beta:
                    break
        return best
    else:
        best = 1000000
        for c in range(COLS):
            if is_valid_move(c):
                drop_disc(c, HUMAN)
                score = minimax(depth - 1,alpha, beta, True)
                undo_move(c)
                if score < best:
                    best = score
                beta = min(beta, score)
                if alpha >= beta:
                    break
        return best
        
def best_move():
    global nodes
    nodes = 0

    best_score = -1000000
    best_col = 0

    for c in range(COLS):
        if is_valid_move(c):
            drop_disc(c, AI)
            score = minimax(DEPTH - 1,-1000000000000,100000000000, False)
            undo_move(c)

            if score > best_score:
                best_score = score
                best_col = c

    return best_col, best_score


# =========================
# GUI + Output + Timing
# =========================
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
Notselected = True

def colour(board , x , y):
    piece = board[y][x]
    if(piece == AI):
        return YELLOW
    if(piece == HUMAN):
        return RED
    return BLACK

game_end = 3

def gui():
    global Notselected
    global DEPTH
    global nodes
    global tm
    global totalcount
    global totaltime
    global game_end
    global val
    pygame.init()
    pygame.display.set_caption("Connect 4")
    squaresize = 100
    radius = int(squaresize / 2 - 5)
    s_width = 7 * squaresize
    s_height = 7 * squaresize
    size = (s_width, s_height)
    screen = pygame.display.set_mode(size)
    my_font = pygame.font.SysFont("monospace", 20, bold=True)
    slider_x = 150
    slider_y = 620
    slider_width = 400
    knob_x = 150  
    dragging = False
    step_size = slider_width // 6
    knob_rect = pygame.Rect(knob_x - (20 // 2), slider_y - 10, 20, 20)
    playing = False
    choosing = True
    column = -1
    while True:
        if(check_win(1)):
            game_end = 1
        if(check_win(2)):
            game_end = -1
        else:
            if(is_full()):
                game_end = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, BLUE, (25, 25, 650, 550))
            for i in range(0,14,2):
                for j in range(0,12,2): 
                    pygame.draw.circle(screen, colour(board,int(i/2),int(j/2)), (73 + (i * radius)+i,73+(j*radius)), radius)##### Made this so instead of display black it checks the board parameter and assgins the colour using the function (colour)
            if Notselected:
                if event.type == pygame.MOUSEBUTTONDOWN:
                        if knob_rect.collidepoint(event.pos):
                                dragging = True

                if event.type == pygame.MOUSEBUTTONUP:
                            dragging = False

                if event.type == pygame.MOUSEMOTION and dragging:
                            mouse_x = event.pos[0]

                            mouse_x = max(slider_x, min(mouse_x, slider_x + slider_width))
                            index = round((mouse_x - slider_x) / step_size)

                            knob_x = slider_x + (index * step_size)
                            knob_rect.x = knob_x - 10
                value_slider = int(((knob_x - slider_x)/step_size)+1)
                text = "Choose difficulty: "+str(value_slider)
                label = my_font.render(text, True, (0, 255, 0))
                screen.blit(label, (230, 577))
                button_rect = pygame.Rect(290, 640, 120, 35)    #select button
                button_rect2 = pygame.Rect(500, 630, 130, 35)   #play again button
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        Notselected = False
                        playing = True
                        DEPTH = value_slider
                current_color = (70, 200, 10)
                pygame.draw.rect(screen, current_color, button_rect, border_radius=12)

                text_surf = my_font.render("SELECT", True, (255, 255, 255))
                text_rect = text_surf.get_rect(center=button_rect.center)
                screen.blit(text_surf, text_rect)

                pygame.draw.line(screen, (255, 255, 255), (slider_x, slider_y), (slider_x + slider_width, slider_y), 5)
                for i in range(7):
                    tick_x = slider_x + (i * step_size)
                    pygame.draw.line(screen, (200, 200, 200), (tick_x, slider_y - 5), (tick_x, slider_y + 5), 2)
                pygame.draw.rect(screen, (255, 0, 0), knob_rect)
                pygame.display.update()
            elif (playing and game_end == 3):
                if(Notselected == False):
                    iter = my_font.render("Iterations : " + str(nodes), True, (0, 255, 0))
                    screen.blit(iter, (25, 670))
                    Ttime = my_font.render("Time : " + f"{tm:.3f}"+"ms", True, (0, 255, 0))
                    screen.blit(Ttime, (500, 670))
                    Ttime = my_font.render("Move Value : " + str(val), True, (0, 255, 0))
                    screen.blit(Ttime, (275, 670))
                    pygame.display.update()  
                column=-1
                choosing = True
                column_rects = [
                    pygame.Rect(25 + (radius*2*i*1.035) , 25, radius*2, 550)
                    for i in range(7)
                ]
                #for rect in column_rects:
                #    pygame.draw.rect(screen, (0, 255, 0), rect, 1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for i, rect in enumerate(column_rects):
                        if rect.collidepoint(event.pos):
                            #print(f"You clicked Column {i + 1}")
                            column = i+1

                            for i in range(6):
                                color_check = screen.get_at((25+radius+((column-1)*2*radius),25+550-radius - (i*2*radius)))
                                if color_check == BLACK:
                                    pygame.draw.circle(screen, RED,(74+((column-1)*(2*radius+2)) , 73+((5-i)*2*radius)),radius)
                                    thinking = my_font.render("AI thinking...", True, (0, 255, 0))
                                    screen.blit(thinking, (50, 620))
                                    break
                            choosing = False
                pygame.display.update()
            if choosing == False:
                if game_end == -1:
                    gameend = my_font.render("AI Won", True, (0, 255, 0))
                    screen.blit(gameend, (315, 600))
                    iter = my_font.render("Total Iterations : " + str(totalcount), True, (0, 255, 0))
                    screen.blit(iter, (25, 670))
                    Ttime = my_font.render("Total Time : " + f"{totaltime:.3f}" +"ms", True, (0, 255, 0))
                    screen.blit(Ttime, (25, 645))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect2.collidepoint(event.pos):
                                game_end = 3
                                Notselected = True
                                return
                    current_color = (78, 128, 18)
                    pygame.draw.rect(screen, current_color, button_rect2, border_radius=12)

                    text_surf = my_font.render("Play again", True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=button_rect2.center)
                    screen.blit(text_surf, text_rect)
                    
                elif game_end == 1:
                    gameend = my_font.render("Player Won", True, (0, 255, 0))
                    screen.blit(gameend, (290, 600))
                    iter = my_font.render("Total Iterations : " + str(totalcount), True, (0, 255, 0))
                    screen.blit(iter, (25, 670))
                    Ttime = my_font.render("Total Time : " + f"{totaltime:.3f}"+"ms", True, (0, 255, 0))
                    screen.blit(Ttime, (25, 645))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if button_rect2.collidepoint(event.pos):
                            game_end = 3
                            Notselected = True
                            return
                    current_color = (78, 128, 18)
                    pygame.draw.rect(screen, current_color, button_rect2, border_radius=12)

                    text_surf = my_font.render("Play again", True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=button_rect2.center)
                    screen.blit(text_surf, text_rect)
                    
                elif game_end == 0:
                    gameend = my_font.render("Draw", True, (0, 255, 0))
                    screen.blit(gameend, (315, 600))
                    iter = my_font.render("Total Iterations : " + str(totalcount), True, (0, 255, 0))
                    screen.blit(iter, (25, 670))
                    Ttime = my_font.render("Total Time : " + f"{totaltime:.3f}"+"ms", True, (0, 255, 0))
                    screen.blit(Ttime, (25, 645))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            if button_rect2.collidepoint(event.pos):
                                game_end = 3
                                Notselected = True
                                return
                    current_color = (78, 128, 18)
                    pygame.draw.rect(screen, current_color, button_rect2, border_radius=12)

                    text_surf = my_font.render("Play again", True, (255, 255, 255))
                    text_rect = text_surf.get_rect(center=button_rect2.center)
                    screen.blit(text_surf, text_rect)
                        
                elif(is_valid_move(column-1) and game_end == 3):
                    drop_disc(column-1,HUMAN)  
                    start_time = time.perf_counter()
                    col , val = best_move()
                    print(col)
                    end_time = time.perf_counter()
                    tm = (end_time - start_time) * 1000
                    totalcount += nodes
                    totaltime += tm
                    if(check_win(1)):
                        game_end = 1
                    else:
                        if(is_full()):
                            game_end = 0      
                    if(game_end == 3):
                        drop_disc(col,AI)
                pygame.display.update()




while(True):
    totalcount = 0
    totaltime = 0
    board = []    

    for r in range(ROWS):   
        row = []  

        for c in range(COLS):   
            row.append(EMPTY)
           

        board.append(row)  


    nodes = 0  
    tm = 0
    val = 0
    gui()
#root.mainloop()