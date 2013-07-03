__author__ = 'win7'
#First thing is to create the globals
#Two states taking input and playing
#http://inventwithpython.com/pygamecheatsheet.png
import pygame,sys
from pygame.locals import*

INPUT=True
PLAYING=False
FPS = 30
WINDOWWIDTH = 400
WINDOWHEIGHT = 400
BOXSIZE=10
GAPSIZE=2
BOARDHEIGHT=15
BOARDWIDTH=15

BOARD_XSPACE=(BOARDWIDTH*BOXSIZE + (BOARDWIDTH-1)*GAPSIZE)
BOARD_YSPACE=(BOARDHEIGHT*BOXSIZE +(BOARDHEIGHT-1)*GAPSIZE)
assert (BOARD_XSPACE<=WINDOWWIDTH),'BOARDWIDTH is too wide for WINDOWWIDTH'
assert (BOARD_YSPACE<=WINDOWHEIGHT),'BOARDHEIGHT is too tall for WINDOWHEIGHT'

XMARGIN=int(WINDOWWIDTH-BOARD_XSPACE)/2
YMARGIN=int(WINDOWHEIGHT-BOARD_YSPACE)/2

# r g b
GRAY= (100,100,100) #BG
BLACK= (0,0,0) #GRID COLOR
WHITE=(255,255,255)#GAPSIZE COLOR
GREEN=(0,155,0)#GRID COLOR ALIVE
LIGHTGREEN=(0,255,0)#GRID COLOR SELECTED

BGCOLOR = GRAY
BOXCOLOR=BLACK#Dead cell color
GAPCOLOR=WHITE
LIVECELLCOLOR=GREEN
HIGHLIGHT=LIGHTGREEN

live_cells=[]
Next_live_cells=[] # Not sure if I have to use this
current_mouse_pos=[0,0]

def generate_dead(): ##Note to self be very careful column here is a reference not a copy
    live_cells[:]=[]
    cell_state=False
    for i in range(BOARDHEIGHT):
        row=[]
        for j in range(BOARDWIDTH):
            row.append(cell_state)
        live_cells.append(row)
    return live_cells

def set_up_display():

    global windowSurfaceObj,FPSCLOCK
    pygame.init()
    FPSCLOCK=pygame.time.Clock()
    windowSurfaceObj = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
    pygame.display.set_caption('Conway\'s Game of Life.')

def check_surrounding(boxx,boxy):
    surrounding=[]
    for x in range(boxx-1,boxx+2):
        row=[]
        for y in range(boxy-1,boxy+2):
            row.append([x,y])
        surrounding.append(row)
    surrounding[(boxx,boxy)]=None
    print(surrounding)


def left_top_coords_box(boxx,boxy):#Changed here

    x=(boxx)*(BOXSIZE+GAPSIZE)+XMARGIN
    y=(boxy)*(BOXSIZE+GAPSIZE)+YMARGIN
    return x,y


def draw_board(window_surface,array):#Why isn't window_surface a local variable?????????

    xtop_left,ytop_left=left_top_coords_box(0,0)
    pygame.draw.rect(window_surface,GAPCOLOR,(xtop_left-1,ytop_left-1,BOARD_XSPACE+2,BOARD_YSPACE+2))
    for i in range(BOARDWIDTH):
        for j in range(BOARDHEIGHT):
            if array[i][j]==True:
                color=LIVECELLCOLOR

            else:
                color=BOXCOLOR
            x,y=left_top_coords_box(i,j)
            pygame.draw.rect(window_surface,color,(x,y,BOXSIZE,BOXSIZE))
    #Code to highlight cube
    if get_box_at_pixel(current_mouse_pos[0],current_mouse_pos[1])!=(None,None):
        boxx,boxy=get_box_at_pixel(current_mouse_pos[0],current_mouse_pos[1])
        x,y=left_top_coords_box(boxx,boxy)
        color= HIGHLIGHT
        pygame.draw.rect(window_surface,color,(x,y,BOXSIZE,BOXSIZE))

    pygame.display.update()

def check_for_quit():
    if pygame.event.get(QUIT):
        pygame.quit()
        sys.exit()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()
        pygame.event.post(event)#put back the KEYUP objects


def draw_start_rect():
    global start_rect
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    start_surface=FONT.render('Start',1,WHITE,GREEN)
    start_rect=start_surface.get_rect()
    start_rect.topleft=(XMARGIN/4,YMARGIN/4)
    windowSurfaceObj.blit(start_surface,start_rect)
    pygame.display.update()

def get_mouse_pos():
    for event in pygame.event.get():
        if event.type == MOUSEMOTION:
            mousex,mousey=event.pos
            current_mouse_pos[0],current_mouse_pos[1]=mousex,mousey
        else:
            pygame.event.post(event) #put back the  event
    return current_mouse_pos[0],current_mouse_pos[1]

def get_box_at_pixel(x,y):
    if (x==None or y == None):
        return None,None
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left,top = left_top_coords_box(boxx,boxy)
            boxrect= pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxrect.collidepoint(x,y):
                return (boxx,boxy)
    return (None,None)



def input():
    mousex,mousey =get_mouse_pos()

    boxx,boxy=get_box_at_pixel(mousex,mousey)
    is_clicked=None
    is_clicked = pygame.event.get(MOUSEBUTTONUP)
    if (boxx!=None and boxy!=None and is_clicked):
        live_cells[boxx][boxy]=not live_cells[boxx][boxy]





def main():#main game loop want to implement stop later but not now
    set_up_display()
    generate_dead()
    check_surrounding(3,3)
    while INPUT:
        draw_start_rect()
        draw_board(windowSurfaceObj,live_cells)
        check_for_quit()
        input()
        FPSCLOCK.tick(FPS)



if __name__ == '__main__':
    main()