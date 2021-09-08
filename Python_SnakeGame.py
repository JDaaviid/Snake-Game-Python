import pygame, sys, random
from pygame.math import Vector2
class FOOD:
    # create an x and y position
    def __init__(self):
        self.randomize()
        
    # draw a square (the food)
    def draw_food(self):
        # create a rectangle
                             #Place the rectangle in the 5th cell (axis X) and in the 4th cell (axis Y)
        food_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        # draw the rectangle
        screen.blit(burger, food_rect)
        

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y) #Store 2D data

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0) # Starts without moving

        # Load images of the snake
        self.head_up = pygame.image.load("Graphics/snake_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/snake_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/snake_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/snake_left.png").convert_alpha()
        
        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()
        
        self.bite_sound = pygame.mixer.Sound("Sounds/eat_sound.mp3")

    def draw_snake(self):
       self.update_head_graphics()
       self.update_tail_graphics()

       for index, block in enumerate(self.body):
           # create a rectangle
           x_pos = int(block.x * cell_size)
           y_pos = int(block.y * cell_size)
           block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
           # what direction is the face heading
           if index == 0:
               screen.blit(self.head, block_rect)
           elif index == len(self.body) - 1: # The last component
               screen.blit(self.tail, block_rect)
           else:
               pygame.draw.rect(screen, (255,89,46), block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0] # The block after the head - head block
        if head_relation == Vector2(1,0): #Left direction.
            self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down
    
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(0,-1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_down
        elif tail_relation == Vector2(1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_left
    
    def move_snake(self): #Execute the method periodically
        body_copy = self.body[:-1] #The third component disappears
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy 
    
    def add_block(self):
       last_block = self.body[-1] 
       self.body.append(last_block)

    def play_bite_sound(self):
        self.bite_sound.play()
    
    def reset(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0) # Starts without moving

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.food = FOOD()
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.food.draw_food()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.snake.body[0] == self.food.pos:
            # reposition the food
            self.food.randomize()
            # add another block to the snake
            self.snake.add_block()
            self.snake.play_bite_sound()

        # Avoid the food from appearing inside the snake body
        for block in self.snake.body[1:]:
            if block == self.food.pos:
                self.food.randomize()
    
    def check_fail(self):
        # check if snake is outside of the screen
        if not (0 <= self.snake.body[0].x < cell_number) or (not 0 <= self.snake.body[0].y < cell_number):
            self.game_over()
        # check if snake hits itself
        for block in self.snake.body[1:]: #Except the head
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_grass(self):
        grass_color = (167,209,61)
    
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3) # Snake starts with 3 blocks
        score_surface = game_font.render(score_text, True, (56,74,12)) #(text, antialias, color)
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center= (score_x, score_y))
        burger_rect = burger.get_rect(midright = (score_rect.left - (cell_size/2), score_rect.centery))
        bg_rect = pygame.Rect(burger_rect.left - 5, burger_rect.top, burger_rect.width + score_rect.width + (10 + cell_size/2), burger_rect.height)

        pygame.draw.rect(screen, (167,209,61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(burger, burger_rect)
        pygame.draw.rect(screen, (56,74,12), bg_rect, 2) # Draw the linewidth ->  2 linewidth


pygame.mixer.pre_init(44100,-16,2,512) # To preprocess the sound           
pygame.init()
cell_size = 30
cell_number = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
pygame.display.set_caption('Snake Game')

burger = pygame.image.load("Graphics/burger.png").convert_alpha()
game_font = pygame.font.Font("Graphics/Stay_and_Shine.ttf", 25) # (font, font_size)

SCREEN_UPDATE = pygame.USEREVENT # Screen updates
pygame.time.set_timer(SCREEN_UPDATE, 150) # Event triggered every 150ms

main_game = MAIN()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)

            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)

            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)

    screen.fill((175,215,70)) # To colorize the trail of the snake constantly
    main_game.draw_elements() # To draw the snake constantly
    pygame.display.update()
    clock.tick(60) # Maximum 60 FPS