import pygame
from pygame.locals import *
from pygame.version import PygameVersion

pygame.init()

#Defining gaming window size and font

Window_width = 500
Window_height = 500

window = pygame.display.set_mode((Window_height, Window_width))
pygame.display.set_caption('BrickBreak')

font = pygame.font.SysFont("Arail", 30) 

# brick color
Orange_brick = (255, 100, 10)
red_brick = (242, 85, 96)
green_brick = (86, 174, 87)
black = (0, 0, 0)
paddle_color = (142, 135, 123)
paddle_outline = (100, 100, 100)

text_col = (79, 82, 140)

game_rows = 6
game_coloumns = 6
clock = pygame.time.Clock()
frame_rate = 60
my_ball = False 
game_over = 0
score = 0
bg = (234, 218, 184)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    window.blit(img, (x, y))


class wall():
    def __init__(self):
        self.width = Window_width//game_coloumns
        self.height = 40

    def create_wall(self):
        self.blocks = []
        #define an empty list for individual block/brick 
        block_individual = []
        for row in range(game_rows):
            #reset the block row list
            block_row = []
            #iterate through columns in that row
            for col in range(game_coloumns):
                #generate x and y positions for each block and create a rectange from that
                block_x = col * self.width
                block_y = row  * self.height 
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                #assign block/brick strenght on row
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1

                #create a list at this point to store the rect and colour data
                block_individual = [rect, strength]
                #append that individual block to block row  
                block_row.append(block_individual)
            #append the row to the full list of blocks
            self.blocks.append(block_row)


    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #assign color to block?brick on strength

                if block[1] == 3:
                    brick_colour = Orange_brick
                elif block[1] == 2:
                    brick_colour = red_brick
                elif block[1] == 1:
                    brick_colour = green_brick            
                pygame.draw.rect(window, brick_colour, block[0])
                pygame.draw.rect(window, bg , (block[0]), 1 )


class paddle():
    def __init__(self):
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1 
        if key[pygame.K_RIGHT] and self.rect.right < Window_width:
            self.rect.x += self.speed
            self.direction = 1 

    def draw(self):
        pygame.draw.rect(window, paddle_color, self.rect)
        pygame.draw.rect(window, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(Window_width/game_coloumns)
        self.x = int((Window_width/2) - (self.width/2))
        self.y = Window_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0


# ball class
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):
        #collision threshold
        collision_thresh = 5
        wall_destroyed = 1 
        row_count = 0
        #start off with the assumption that the wall is destroyed completely
        for row in wall.blocks:
            item_count = 0
            for item in row:
                #check collision with each block
                if self.rect.colliderect(item[0]):
                    #check if collision was from above
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    #check if collision was from below
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    #check if collision was from left
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x*= -1
                    #check if collision was from right
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1

                    #reduce the block's strength by doing damage to it
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0) 

                #check if block still exists, in which case the wall is not destroyed
                if wall.blocks[row_count][item_count] != (0, 0, 0, 0):
                    wall_destroyed = 0
                #increase item_count
                item_count += 1
            #increase row_count 
            row_count += 1

        if wall_destroyed == 1:
            self.game_over = 1
        #check for collision with walls
        if self.rect.left < 0 or self.rect.right > Window_width:
            self.speed_x *= -1

        #check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speed_y *= -1 
        if self.rect.bottom > Window_height:
            self.game_over = -1

        #check for collision with paddle
        if self.rect.colliderect(player_paddle):
            #check if collision from the top
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
                else:
                    self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over 

    def draw(self):
        pygame.draw.circle(window, paddle_color,(self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(window, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),self.ball_rad, 2 )

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad 
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad*2, self.ball_rad*2)
        self.speed_max = 5
        self.speed_x = 4
        self.speed_y = -4
        self.game_over = 0



wall = wall()
wall.create_wall() 

player_paddle = paddle()
ball = game_ball(player_paddle.x + (player_paddle.width //2), player_paddle.y - player_paddle.height) 

run = True
while run:
    clock .tick(frame_rate)

    window.fill(bg)

    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if my_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            my_ball = False

    #print instruction
    if not my_ball:
        if game_over == 0:
            draw_text('Click anywhere to start', font, text_col, 140, Window_height//2 + 100)
        elif game_over == 1:
            draw_text('You Won', font, text_col, 200, Window_height//2 + 50)
            draw_text('Click anywhere to start', font, text_col, 140, Window_height//2 + 100)
        elif game_over == -1:
            draw_text('You Lost', font, text_col, 200, Window_height//2 + 50)
            draw_text('Click anywhere to start', font, text_col, 140, Window_height//2 + 100)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and my_ball == False:
            my_ball = True
            ball.reset(player_paddle.x + (player_paddle.width //2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()