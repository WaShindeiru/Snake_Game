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


class Body(pygame.sprite.Sprite):
    def __init__(self, x, y, x_, y_):
        super().__init__()

        self.image = pygame.image.load("./images/body.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.x_speed = x_
        self.y_speed = y_

    # def update(self):
    #     self.rect.x += self.x_speed
    #     self.rect.y += self.y_speed


class Head(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.x_loc = 50
        self.y_loc = 50

        self.image = pygame.image.load("./images/head.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.x_loc, self.y_loc))

        self.x_speed = 50
        self.y_speed = 50

        self.body_list = list()
        self.food = 0

        self.previous_possision = (0, 0)

    def move_update(self,x,y):
        self.x_speed = x
        self.y_speed = y

    def update(self):
        self.previous_possision = (self.rect.x, self.rect.y)
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

        for a in range(len(self.body_list)-2, -1, -1):
            self.body_list[a+1].rect.topleft = self.body_list[a].rect.topleft

        if self.body_list:
            self.body_list[0].rect.topleft = self.previous_possision

    def feed(self):
        self.food += 1
        
        self.body_list.append(Body(self.previous_possision[0], self.previous_possision[1], self.x_speed, self.y_speed))


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
        time = time - 500*i
        # print(time)
        if time > 500:
            # print(time)
            i = i + 1
            group.update()

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
                group.add(head.body_list[-1])
                Body_group.add(head.body_list[-1])

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