import pygame
from random import randrange
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WIDTH = 800
HEIGHT = 800
BLOCK = 40
DIRECTION_MATRIX = [
[0, 5, 0, 2],
[3, 1, 2, 1],
[0, 4, 0, 3],
[4, 1, 5, 1]]

class Body(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, previous):
        super().__init__()
        self.direction = direction 
        self.previous = previous

        self.body_sprite = [pygame.image.load("./images/tile001.png").convert_alpha(),
        pygame.image.load("./images/tile007.png").convert_alpha(),
        pygame.image.load("./images/tile005.png").convert_alpha(),
        pygame.image.load("./images/tile012.png").convert_alpha(),
        pygame.image.load("./images/tile002.png").convert_alpha(),
        pygame.image.load("./images/tile000.png").convert_alpha()]

        self.tail_sprite = [pygame.image.load("./images/tile014.png").convert_alpha(),
        pygame.image.load("./images/tile013.png").convert_alpha(),
        pygame.image.load("./images/tile018.png").convert_alpha(),
        pygame.image.load("./images/tile019.png").convert_alpha()]
        self.image = self.body_sprite[0]

        if self.previous != -1:
            self.image = self.body_sprite[DIRECTION_MATRIX[self.direction][self.previous]]

        else:
            self.image = self.tail_sprite[self.direction]
    
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

    def update(self):
        if self.previous == -1:
            self.image = self.tail_sprite[self.direction]



class Head(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x_loc = 50
        self.y_loc = 50

        self.head_sprite = [pygame.image.load("./images/tile004.png").convert_alpha(),
        pygame.image.load("./images/tile003.png").convert_alpha(), 
        pygame.image.load("./images/tile008.png").convert_alpha(),
        pygame.image.load("./images/tile009.png").convert_alpha()]

        self.image = self.head_sprite[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_loc, self.y_loc)

        self.x_speed = 50
        self.y_speed = 50

        self.body_queue = list()
        self.food = 0
        self.direction = 0


    def move_update(self,x,y):
        self.x_speed = x
        self.y_speed = y

    def update(self):
        if self.x_speed > 0:
            self.image = self.head_sprite[0]
            self.direction = 0

        elif self.x_speed < 0:
            self.image = self.head_sprite[2]
            self.direction = 2

        elif self.y_speed < 0:
            self.image = self.head_sprite[1]
            self.direction = 1

        elif self.y_speed > 0:
            self.image = self.head_sprite[3]
            self.direction = 3
            
        if self.body_queue:
            self.body_queue.insert(0, Body(self.rect.x, self.rect.y, self.direction, self.body_queue[0].direction))
        else:
            self.body_queue.insert(0, Body(self.rect.x, self.rect.y, self.direction, -1))
        while len(self.body_queue) > self.food:
            self.body_queue.pop().kill()
        if self.body_queue:
            self.body_queue[-1].previous = -1

        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        if self.rect.right > HEIGHT:
            self.rect.x = 0
        
        elif self.rect.left < 0:
            self.rect.x = HEIGHT - BLOCK
        
        if self.rect.y < 0:
            self.rect.y = WIDTH - BLOCK
        
        elif self.rect.bottom > HEIGHT:
            self.rect.y = 0

    def feed(self):
        self.food += 1

        
        # self.body_list.append(Body(self.previous_possision[0], self.previous_possision[1], self.x_speed, self.y_speed))


class Apple(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
    
        self.image = pygame.image.load("images/apple.png")
        self.rect = self.image.get_rect()
        
        self.rect.x = randrange(0, 800, 50)
        self.rect.y = randrange(0, 800, 50)

    def find_new_home(self):
        self.rect.x = randrange(0, 800, 50)
        self.rect.y = randrange(0, 800, 50)


def main():
    pygame.init()
 
    # Set the width and height of the screen [width, height]
    size = (800, 800)
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("My Game")
    
    # Loop until the user clicks the close button.
    done = False
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    grass = pygame.image.load("./images/background.png").convert()
    i=0
    apple_count = 0

    head = Head()
    group = pygame.sprite.Group()
    group.add(head)

    fruits = pygame.sprite.Group()
    Body_group = pygame.sprite.Group()

    # -------- Main Program Loop -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    head.move_update(-50, 0)

                elif event.key == pygame.K_RIGHT:
                    head.move_update(50, 0)

                elif event.key == pygame.K_UP:
                    head.move_update(0, -50)

                elif event.key == pygame.K_DOWN:
                    head.move_update(0, 50)
    
        # --- Game logic  should go here
        time = pygame.time.get_ticks()
        time = time - 200*i
        # print(time)
        if time > 200:
            # print(time)
            i = i + 1
            group.update()
            if head.food > 0:
                Body_group.add(head.body_queue[0])
                group.add(head.body_queue[0])
            Body_group.update()

        if apple_count == 0:
            apple_count = 1
            apple = Apple()
            group.add(apple)
            fruits.add(apple)

        fruit_list = pygame.sprite.spritecollide(head, fruits, False)
        if fruit_list:
            for fruit in fruit_list:
                fruit.find_new_home()
                fruit_list.pop()
                head.feed()

        if pygame.sprite.spritecollide(head, Body_group, False):
            pygame.time.wait(5000)
        # --- Screen-clearing code goes here
    
        # Here, we clear the screen to white. Don't put other drawing commands
        # above this, or they will be erased with this command.
    
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.blit(grass, (0, 0))
    
        # --- Drawing code should go here
        group.draw(screen)

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    
        # --- Limit to 60 frames per second
        clock.tick(30)
    
    # Close the window and quit.
    pygame.quit()

main()