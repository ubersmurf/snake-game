import pygame
import random

#game
class Game():
    
    def __init__(self):
        pygame.init()
        
        self.previous_scores = []
    
        #colors
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 102)
        self.black = (0, 0, 0)
        self.red = (213, 50, 80)
        self.green = (0, 255, 0)
        self.blue = (50, 153, 213)
        
        #setting up the window
        self.dis_width = 1920
        self.dis_height = 1080
        self.dis = pygame.display.set_mode((self.dis_width, self.dis_height))
        pygame.display.set_caption('Snake Game by Ubersmurf')
        
        #snake speed
        self.clock = pygame.time.Clock()
        self.snake_block = 25
        self.snake_speed = 60

        #fonts
        self.font_style = pygame.font.SysFont("bahnschrift", 25)
        self.score_font = pygame.font.SysFont("comicsansms", 35)

        self.load_data()
        
    #load highest score
    def load_data(self):
        with open("directory_name/highest_score.txt", 'r+') as f:
            try:
                self.high_score = int(f.read())
            except:
                self.high_score = 0
    
    #gameloop
    def gameLoop(self):
        
        def Your_score(score):
            value = self.score_font.render("Your Score: " + str(score), True, self.yellow)
            self.dis.blit(value, [0, 0])  
            
        def our_snake(snake_block, snake_list):
            for x in snake_list:
                pygame.draw.rect(self.dis, self.white, [x[0], x[1], snake_block, snake_block])
        
        def message(msg, color):
            mesg = self.font_style.render(msg, True, color)
            self.dis.blit(mesg, [self.dis_width / 6, self.dis_height / 3])
        
        def print_highest_score(score):
            value = self.score_font.render("Highest Score: " + str(score), True, self.yellow)
            self.dis.blit(value, [0,50])
        
        game_over = False
        game_close = False
    
        #snakes starting point
        x1 = self.dis_width / 2
        y1 = self.dis_height / 2
        #snakes starting moving speed
        x1_change = 0
        y1_change = 0
    
        snake_List = []
        Length_of_snake = 1

        #food locations
        food_blue_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        food_blue_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
        food_green_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        food_green_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
        food_red_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
        food_red_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
    
        while not game_over:
    
            #if game over
            while game_close == True:
                self.dis.fill(self.black)
                message("You Lost! Press C-Play Again or Q-Quit", self.red)
                Your_score(Length_of_snake - 1)
                pygame.display.update()
    
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            game_over = True
                            game_close = False
                        if event.key == pygame.K_c:
                            Game().gameLoop()
            
            #snake movement script
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        x1_change = -self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_d:
                        x1_change = self.snake_block
                        y1_change = 0
                    elif event.key == pygame.K_w:
                        y1_change = -self.snake_block
                        x1_change = 0
                    elif event.key == pygame.K_s:
                        y1_change = self.snake_block
                        x1_change = 0

            #if snake touches the borders
            if x1 >= self.dis_width:       
                x1 = self.snake_block
            elif x1 <= 0:
                x1 = self.dis_width-self.snake_block
            elif y1 >= self.dis_height:
                y1 = self.snake_block
            elif y1 <= 0:
                y1 = self.dis_height-self.snake_block
            x1 += x1_change
            y1 += y1_change
            
            #drawing foods
            self.dis.fill(self.black)
            pygame.draw.rect(self.dis, self.blue, [food_blue_x, food_blue_y, self.snake_block, self.snake_block])
            pygame.draw.rect(self.dis, self.green, [food_green_x, food_green_y, self.snake_block, self.snake_block])
            pygame.draw.rect(self.dis, self.red, [food_red_x, food_red_y, self.snake_block, self.snake_block])
            
            #making snake longer
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
            our_snake(self.snake_block, snake_List)
            Your_score(Length_of_snake - 1)
            print_highest_score(self.high_score)
    
            pygame.display.update()
            
            #defining rectangels of game objects
            player_rect = pygame.Rect(x1,y1,self.snake_block, self.snake_block)
            food_blue_rect = pygame.Rect(food_blue_x,food_blue_y,self.snake_block, self.snake_block)
            food_green_rect = pygame.Rect(food_green_x, food_green_y, self.snake_block, self.snake_block)
            food_red_rect = pygame.Rect(food_red_x, food_red_y, self.snake_block, self.snake_block)
    
            #detecting the collision between snake and foods
            if player_rect.colliderect(food_blue_rect):
                food_blue_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                food_blue_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 1
            elif player_rect.colliderect(food_green_rect):
                food_green_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                food_green_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 2
            elif player_rect.colliderect(food_red_rect):
                food_red_x = round(random.randrange(0, self.dis_width - self.snake_block) / 10.0) * 10.0
                food_red_y = round(random.randrange(0, self.dis_height - self.snake_block) / 10.0) * 10.0
                Length_of_snake += 3
                
            self.clock.tick(self.snake_speed)
        
        #if snake beated new record save the new score
        if Length_of_snake-1 > self.high_score:
            self.high_score = Length_of_snake - 1
            print_highest_score(self.high_score)
            with open("directory_name/highest_score.txt", "w") as f:
                f.write(str(self.high_score))
        else:
            print_highest_score(self.high_score)
        
        #saving previous scores
        self.previous_scores.append(Length_of_snake - 1)
        with open("directory_name/previous_scores.txt", "a") as f:
            for n in zip(self.previous_scores):
                f.write(f'score {n[0]}\n')
        
    
        pygame.quit()
        quit()

Game().gameLoop()
