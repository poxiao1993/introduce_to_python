# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists    
    ball_pos = [0, 0]
    ball_vel = [0, 0]
    ball_pos[0] = WIDTH / 2
    ball_pos[1] = HEIGHT / 2    
    if direction == LEFT:
        ball_vel[0] = -random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)
    elif direction == RIGHT:
        ball_vel[0] = random.randrange(2, 4)
        ball_vel[1] = -random.randrange(1, 3)                     

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = paddle1_pos
    paddle1_vel = 0
    paddle2_vel = 0
    if LEFT == True:
        spawn_ball(LEFT)  
    elif RIGHT == True:
        spawn_ball(RIGHT) 

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel     
    #print position
    #draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball   
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    if ball_pos[1] < BALL_RADIUS:
        ball_pos[1] = BALL_RADIUS
        ball_vel[1] = -ball_vel[1]
    elif ball_pos[1] > (HEIGHT - 1 - BALL_RADIUS):
        ball_pos[1] = HEIGHT - 1 - BALL_RADIUS
        ball_vel[1] = -ball_vel[1]        
    elif (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH):        
        ball_pos[0] = BALL_RADIUS + PAD_WIDTH
        ball_vel[0] = -ball_vel[0]        
    elif ball_pos[0] >= (WIDTH - 1 - BALL_RADIUS - PAD_WIDTH):        
        ball_pos[0] = WIDTH - 1 - BALL_RADIUS - PAD_WIDTH
        ball_vel[0] = -ball_vel[0]    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'white', 'white')
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    if paddle1_pos <= 0:
        paddle1_pos = 0
    if paddle1_pos >= HEIGHT - PAD_HEIGHT:
        paddle1_pos = HEIGHT - PAD_HEIGHT
    if paddle2_pos <= 0:
        paddle2_pos = 0
    if paddle2_pos >= HEIGHT - PAD_HEIGHT:
        paddle2_pos = HEIGHT - PAD_HEIGHT
    # draw paddles
    canvas.draw_polygon([(HALF_PAD_WIDTH, paddle1_pos), (HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT)], PAD_WIDTH, 'white')
    canvas.draw_polygon([(WIDTH - HALF_PAD_WIDTH, paddle2_pos), (WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT)], PAD_WIDTH, 'white')
    # determine whether paddle and ball collide    
    if ball_pos[0] == BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1] < paddle1_pos or ball_pos[1] > paddle1_pos + PAD_HEIGHT):
            score2 += 1        
            spawn_ball(RIGHT)
        else:
            ball_vel[0] += 1
    if ball_pos[0] == WIDTH - 1 - BALL_RADIUS - PAD_WIDTH:
        if ball_pos[1] < paddle2_pos or ball_pos[1] > paddle2_pos + PAD_HEIGHT:
            score1 += 1          
            spawn_ball(LEFT)
        else:
            ball_vel[0] -= 1
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4 - 10, 60], 60, 'white')
    canvas.draw_text(str(score2), [WIDTH / 4 * 3 - 10, 60], 60, 'white')
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 5
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = -5 
    elif chr(key) == 'W':                
        paddle1_vel = -5
    elif chr(key) == 'S':
        paddle1_vel = 5             
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0        
    elif key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0        
    elif chr(key) == 'W':        
        paddle1_vel = 0
    elif chr(key) == 'S':
        paddle1_vel = 0  
    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.add_button('Reset', new_game, 100)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()
