import pygame,random,time,sys
import math 
pygame.init()
pygame.font.init()
#game variables
FONT = pygame.font.SysFont('franklingothicmedium',40)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
SPACESHIP_WIDTH,SPACESHIP_HEIGHT = 70,70
WIDTH,HEIGHT =1000,600
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Space Shooter")
SPACEBG = pygame.image.load('cont.jpg')
SPACE = pygame.transform.scale(SPACEBG,(WIDTH,HEIGHT))
SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load('spaceship.png'),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
SPACESHIP = pygame.transform.rotate(SPACESHIP_IMAGE,270) 
BLUE_SPACESHIP_IMAGE = pygame.transform.scale(pygame.image.load('blue_ship.png'),(SPACESHIP_WIDTH,SPACESHIP_HEIGHT))
BLUE_SPACESHIP = pygame.transform.rotate(BLUE_SPACESHIP_IMAGE,270)
SPACE_MENU_IMAGE = pygame.image.load('space.png')
SPACE_MENU_BG = pygame.transform.scale(SPACE_MENU_IMAGE,(WIDTH,HEIGHT))
GAME_OVER_IMAGE = pygame.image.load('game_over.png')
First_controls_img = pygame.transform.scale(pygame.image.load('asdw and space.png'),(400,300))
Second_controls_img = pygame.transform.scale(pygame.image.load('arrows with enter.png'),(400,300))
FPS = 60
SPEED = 7
laser_SPEED = 10
BORDER = pygame.Rect(200,0,1,HEIGHT)
level = 0
enemy_vel = 30
img_width = SPACEBG.get_width()
scroll = 0
slides = math.ceil(WIDTH / img_width) +1
top_enemy = None
bottom_enemy = None
player_health = 15
second_player_health = 15
max_player_health = 15
wavelength = 5
wave = 0
highest_wave= 0
#load button images

exit_img = pygame.image.load('exit_btn.png').convert_alpha()
play_img = pygame.image.load('play_btn.png').convert_alpha()
back_img = pygame.image.load('back_btn.png').convert_alpha()
resume_img = pygame.image.load('resume_btn.png').convert_alpha()
quit_img = pygame.image.load('quit_btn.png').convert_alpha()
controls_img = pygame.image.load('controls_btn.png').convert_alpha()
two_player_img = pygame.image.load('2player_btn.png').convert_alpha()
one_player_img = pygame.image.load('1player_btn.png').convert_alpha()
enemy_img = pygame.transform.scale(pygame.image.load('alien_green.png').convert_alpha(),(50,50))
powerup_img = pygame.transform.scale(pygame.image.load('lightning_bolt.png').convert_alpha(),(50,50))
enemy_pic = pygame.transform.rotate(enemy_img,270)
enemies = []
max_lasers = 3
powerup_on_screen = False


#emeny class
class Enemy:
    def __init__(self, x, y, width, height, speed, image):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 1  # 1 means move down, -1 means move up
        self.image = image
        self.x = x
        self.y = y

    def update(self):
        self.rect.y += self.speed * self.direction
    
    def get_rect(self):
        return self.rect

    def get_x_coord(self):
        return self.rect.x

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
    def shoot(self, enemy_lasers):
        laser = pygame.Rect(
            self.rect.x,
            self.rect.y + self.rect.height // 2 - 2,
            10,
            5,
        )
        enemy_lasers.append(laser)
    def move(self):
        self.rect.x -= self.speed
#power up class
class PowerUp:
    def __init__(self, x, y, width, height, image):
        self.image = image
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.spawn_time = time.time()  # record the time when the power-up spawned
        self.collected = False
        self.expired = False

    def collide(self, ship):
        if self.rect.colliderect(ship):
            self.collected = True

    def should_disappear(self):
        # check if the power-up has been spawned for more than 3 seconds
        time_on_screen = time.time() - self.spawn_time
        if time_on_screen > 3:
            self.expired = True

    def draw(self, surface):
        if not self.collected and not self.expired:
            surface.blit(self.image, self.rect)
#button class
class Button():
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.state = "up"

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()
        
		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.state == "up":
				self.state = "down"
			elif pygame.mouse.get_pressed()[0] == 0 and self.state == "down":
				self.state = "clicked"
				action = True

		if self.state == "clicked":
			self.state = "up"

		#draw button on WINDOW
		surface.blit(self.image, (self.rect.x, self.rect.y))
        
		return action
#create button instances
play_button = Button(WIDTH//2,150,play_img,0.8)
exit_button = Button(WIDTH//2,250,exit_img,0.8)
back_button = Button(WIDTH//2,350,back_img,0.8)
back_button2 = Button(WIDTH//2,400,back_img,0.8)
back_button3 = Button(50,HEIGHT - 30,back_img,0.3)
resume_button = Button(WIDTH//2 - 10,150,resume_img,0.9)
quit_button = Button(WIDTH//2,350,quit_img,0.9)
controls_button = Button(WIDTH//2,380,controls_img,0.8)
two_player_button = Button(WIDTH//2,280,two_player_img,0.8)
one_player_button = Button(WIDTH//2,150,one_player_img,0.8)

#ship movement
def ship_movement(pressed_keys,ship):
    if pressed_keys[pygame.K_a] and ship.x - SPEED > 0 :#left
        ship.x -= SPEED
    if pressed_keys[pygame.K_d] and ship.x + SPEED + SPACESHIP_WIDTH < BORDER.x:#right
        ship.x += SPEED
    if pressed_keys[pygame.K_w] and ship.y - SPEED > 0 :#UP
        ship.y -= SPEED
    if pressed_keys[pygame.K_s] and ship.y + SPEED + SPACESHIP_HEIGHT  < HEIGHT:#DOWN
        ship.y += SPEED




#laser handling 
def handle_lasers(ship,lasers, enemies, is_enemy=False):
    for laser in lasers:
        if is_enemy:
            laser.x -= laser_SPEED  # move laser towards player
        else:
            laser.x += laser_SPEED  # move laser towards enemies
        for enemy in enemies:
            if enemy.rect.colliderect(laser) and not is_enemy:
                enemies.remove(enemy)
                lasers.remove(laser)
        if laser.x < 0 or laser.x > WIDTH:
            lasers.remove(laser)
        
        if laser.colliderect(ship):
                lasers.remove(laser)
                global player_health
                player_health -= 2
    for enemy in enemies:
        if enemy.rect.colliderect(ship):
            enemies.remove(enemy)
            player_health -= 4

        
#draw WINDOW
def draw_WINDOW(ship, lasers, enemies, enemy_lasers,power_up):
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    global scroll
    for i in range(0,slides):
        WINDOW.blit(SPACE,(i*WIDTH+scroll,0))  
    scroll -= 6
    if abs(scroll )> WIDTH:
        scroll = 0 

    WINDOW.blit(SPACESHIP,(ship.x,ship.y))

    for laser in lasers:
        pygame.draw.rect(WINDOW, WHITE, laser)
    for laser in enemy_lasers:
        pygame.draw.rect(WINDOW, RED, laser)
    for enemy in enemies:
        enemy.draw(WINDOW)
   
    # Draw power-up if it is on the screen
    if power_up:
        power_up.draw(WINDOW)

    #Draw ships healthbar to screen
    global player_health
    # Draw the red rectangle vertically
    red_rect = pygame.Rect(ship.x - 10, ship.y, 10, SPACESHIP_IMAGE.get_height())
    pygame.draw.rect(WINDOW, RED, red_rect)

    # Draw the green rectangle vertically
    green_rect = pygame.Rect(ship.x - 10, ship.y + SPACESHIP_IMAGE.get_height() - SPACESHIP_IMAGE.get_height() * (player_health / max_player_health), 10, SPACESHIP_IMAGE.get_height() * (player_health / max_player_health))
    pygame.draw.rect(WINDOW, GREEN, green_rect)
    pygame.display.update()
    

def Pause():
    running = True
    while running:
        if resume_button.draw(WINDOW):
            running = False
        if back_button.draw(WINDOW) :
            main_menu()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

# Function to create a random-spawning wave of enemies
def generate_enemies(game_mode):
    if game_mode == 1:
        enemies = []
        enemy_width = 50
        enemy_height = 50
        enemy_margin = 10
        enemies_per_row = 8
        top_enemy = None
        bottom_enemy = None
        # code to generate enemies for game mode 1
        for row in range(5):
            for col in range(enemies_per_row):
                x = col * (enemy_width + enemy_margin) + WIDTH - (
                    enemies_per_row * (enemy_width + enemy_margin) + enemy_margin
                ) - 50
                y = row * (enemy_height + enemy_margin) + 50
                enemy = Enemy(x, y, enemy_pic.get_width(), enemy_pic.get_height(), 1, enemy_pic)
                enemies.append(enemy)
                if top_enemy is None or enemy.rect.y < top_enemy.rect.y:
                    top_enemy = enemy
                if bottom_enemy is None or enemy.rect.y > bottom_enemy.rect.y:
                    bottom_enemy = enemy
        return enemies, top_enemy, bottom_enemy
    elif game_mode == 2:
        enemies = []
        # code to generate enemies for game mode 2
        global wavelength
        for i in range(int(wavelength)):
            while True: 
                # Create a new enemy
                enemy = Enemy(random.randrange(WIDTH, WIDTH + 500), random.randrange(50, HEIGHT-50),enemy_pic.get_width(), enemy_pic.get_height(), 2,enemy_pic)
                # Check if the new enemy overlaps with any existing enemy
                overlaps = False
                for existing_enemy in enemies:
                    if existing_enemy.rect.colliderect(enemy.rect):
                        overlaps = True
                        break
                # If the new enemy doesn't overlap with any existing enemy, add it to the list and exit the loop
                if not overlaps:
                    enemies.append(enemy)
                    break
        
        top_enemy = enemies[0]
        bottom_enemy = enemies[-1]
        return enemies, top_enemy, bottom_enemy
    
#MAIN video game loop
def Single_Player():
    pygame.init()
    lasers = []
    ship = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    top_enemy = None
    bottom_enemy = None
    enemy_lasers=[]
    game_mode = 0
    enemies = []
    clock = pygame.time.Clock()
    run = True
    global lost,player_health,wave,highest_wave
    lost = False
    first_wave = True
    power_up = None
    player_health = 15
    shot_probability = 0.001
    start_time = 0
    wave = 0
    max_lasers = 3 
    while run:
        clock.tick(FPS)
        # check if all enemies are dead
        if len(enemies) == 0:
            # choose a new game mode randomly
            game_mode = random.randint(1, 2)
            enemies, top_enemy, bottom_enemy = generate_enemies(game_mode)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check for timer event to restore max lasers
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Pause()  

                if event.key == pygame.K_SPACE and len(lasers)<max_lasers:
                    laser = pygame.Rect(
                        ship.x + SPACESHIP_WIDTH,
                        ship.y + SPACESHIP_HEIGHT // 2 - 2,
                        10,
                        5,
                    )
                    lasers.append(laser)

        pressed_keys = pygame.key.get_pressed()
        ship_movement(pressed_keys, ship)
        for enemy in enemies:
            if game_mode==1:
                enemy.update()
                if random.random() < shot_probability:  # adjust the probability of shooting
                    enemy.shoot(enemy_lasers)
        handle_lasers(ship,lasers,enemies)
        handle_lasers(ship,enemy_lasers,enemies, is_enemy=True)
        # update enemies
        if game_mode ==1:
            for enemy in enemies:
                enemy.update()
                if enemy.rect.y < top_enemy.rect.y:
                    top_enemy = enemy
                elif enemy.rect.y > bottom_enemy.rect.y:
                    bottom_enemy = enemy
        else:
            pass
        # check if top or bottom enemy has reached the screen edge
        if game_mode == 1 and top_enemy and bottom_enemy:
            if top_enemy.rect.top <= 0 or bottom_enemy.rect.bottom >= HEIGHT:
                for enemy in enemies:
                    enemy.direction *= -1
        else:
            pass

        if game_mode ==2:
            for enemy in enemies:
                enemy.move()

                if random.random() < shot_probability:
                    enemy.shoot(enemy_lasers)
                if enemy.get_x_coord()+ enemy_img.get_width()<0:
                    enemies.remove(enemy)
                    player_health -=0.5

        #create a power up
        global powerup_on_screen
        if powerup_on_screen:
            power_up.should_disappear()
            power_up.collide(ship)
            
            
            if power_up.collected or power_up.expired:
                powerup_on_screen = False
        else:
        # spawn a new power-up
            if random.random() < 0.0005:
                power_up = PowerUp(random.randrange(0,200), random.randrange(50, HEIGHT-50),
                                    powerup_img.get_width(), powerup_img.get_height(), powerup_img)
                powerup_on_screen = True
        
        # Give power-up
        if power_up:
           if power_up.rect.colliderect(ship):
        # Power-up collected, set max lasers to 6
            max_lasers = 6
            start_time = time.time()
        if( time.time() - start_time)>=5:
            max_lasers = 3
        draw_WINDOW(ship, lasers, enemies, enemy_lasers,power_up)
        if player_health <=0:
            WINDOW.blit(GAME_OVER_IMAGE,(WIDTH//2 - GAME_OVER_IMAGE.get_width()//2,HEIGHT//2 - GAME_OVER_IMAGE.get_height()//2))
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
        if len(enemies) == 0 or first_wave:
            # Increment the wave counter
            wave += 1
            #Increment the shot probability and wavelength to increase game difficulty
            global wavelength
            wavelength += 0.5
            shot_probability += 0.0001
            # Display the wave number
            wave_text = FONT.render(f"Wave {wave}",False, WHITE)
            wave_rect = wave_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WINDOW.blit(wave_text, wave_rect)
            pygame.display.update()
            pygame.time.delay(2000)  
            lasers.clear()
            first_wave = False


        pygame.display.update()

def controls():
    looping = True
    while looping:
    
        WINDOW.blit(SPACE_MENU_BG,(0,0))
        controls_text1 = FONT.render("First Player Controls",False, WHITE)
        controls_text1_rect = controls_text1.get_rect(center=(200, 100))
        WINDOW.blit(controls_text1, controls_text1_rect)

        controls_text2 = FONT.render("Second Player Controls",False, WHITE)
        controls_text2_rect = controls_text2.get_rect(center=(750, 100))
        WINDOW.blit(controls_text2, controls_text2_rect)

        WINDOW.blit(First_controls_img,(10,200))
        WINDOW.blit(Second_controls_img,(600,200))
        
            
        if back_button3.draw(WINDOW):
            
            looping = False
            
       
        for event in pygame.event.get ():
        
            if event.type == pygame.QUIT:
                looping = False
        pygame.display.update()
# funciton to keep track of the high score
def high_score():
    global wave,highest_wave
    if wave > highest_wave:
        highest_wave = wave
    high_score_text = FONT.render(f"Single Player HIGH SCORE is wave: {highest_wave}",False, RED)
    high_score_rect = high_score_text.get_rect(center=(WIDTH//2, HEIGHT - 100))
    WINDOW.blit(high_score_text, high_score_rect)
    pygame.display.update()
#setting up a main menu/GUI
def main_menu():
    looping = True
    while looping:
    
        WINDOW.blit(SPACE_MENU_BG,(0,0))

        if play_button.draw(WINDOW):
            print("playing")
            Player_select()
            
        if exit_button.draw(WINDOW):
            
            looping = False
            
        if controls_button.draw(WINDOW):
            controls()
        for event in pygame.event.get ():
        
            if event.type == pygame.QUIT:
                looping = False
        pygame.display.update()
    pygame.quit()
       
def Player_select():
    looping = True
    while looping:
        WINDOW.blit(SPACE_MENU_BG,(0,0))
        if one_player_button.draw(WINDOW):
            Single_Player()
        if two_player_button.draw(WINDOW):
            Two_Player()
        if back_button2.draw(WINDOW):
            main_menu()

        high_score()
        for event in pygame.event.get ():
        
            if event.type == pygame.QUIT:
                looping = False
        pygame.display.update()
######################################################
#The follwing sections of code are solely for the two player mode


#laser handling 
def handle_lasers_two_player(ship,second_ship,lasers, enemies, is_enemy=False):
    for laser in lasers:
        if is_enemy:
            laser.x -= laser_SPEED  # move laser towards player
        else:
            laser.x += laser_SPEED  # move laser towards enemies
        for enemy in enemies:
            if enemy.rect.colliderect(laser) and not is_enemy:
                enemies.remove(enemy)
                lasers.remove(laser)
        if laser.x < 0 or laser.x > WIDTH:
            lasers.remove(laser)
        
        if laser.colliderect(ship):
                lasers.remove(laser)
                global player_health
                player_health -= 2
        if laser.colliderect(second_ship):
                lasers.remove(laser)
                global second_player_health
                second_player_health -= 2
    for enemy in enemies:
        if enemy.rect.colliderect(ship):
            enemies.remove(enemy)
            player_health -= 4
        if enemy.rect.colliderect(second_ship):
            enemies.remove(enemy)
            second_player_health -= 4

#ship movement
def second_ship_movement(pressed_keys,right_ship):
    if pressed_keys[pygame.K_LEFT] and right_ship.x - SPEED > 0 :#left
        right_ship.x -= SPEED
    if pressed_keys[pygame.K_RIGHT] and right_ship.x + SPEED + SPACESHIP_WIDTH < BORDER.x :#right
        right_ship.x += SPEED
    if pressed_keys[pygame.K_UP] and right_ship.y - SPEED > 0 :#UP
        right_ship.y -= SPEED
    if pressed_keys[pygame.K_DOWN] and right_ship.y + SPEED + SPACESHIP_HEIGHT  < HEIGHT:#DOWN
        right_ship.y += SPEED
 

def TWO_PLAYER_DRAW_WINDOW(ship,second_ship, lasers,second_lasers, enemies, enemy_lasers,power_up):
    pygame.draw.rect(WINDOW,BLACK,BORDER)
    global scroll
    for i in range(0,slides):
        WINDOW.blit(SPACE,(i*WIDTH+scroll,0))  
    scroll -= 6
    if abs(scroll )> WIDTH:
        scroll = 0 

    WINDOW.blit(SPACESHIP,(ship.x,ship.y))
    WINDOW.blit(BLUE_SPACESHIP,(second_ship.x,second_ship.y))

    for laser in lasers:
        pygame.draw.rect(WINDOW, WHITE, laser)
    for laser in second_lasers:
        pygame.draw.rect(WINDOW, WHITE, laser)    
    for laser in enemy_lasers:
        pygame.draw.rect(WINDOW, RED, laser)
    for enemy in enemies:
        enemy.draw(WINDOW)
   
    # Draw power-up if it is on the screen
    if power_up:
        power_up.draw(WINDOW)

    #Draw main ship's healthbar to screen
    global player_health,second_player_health
    # Draw the red rectangle vertically
    red_rect = pygame.Rect(ship.x - 10, ship.y, 10, SPACESHIP_IMAGE.get_height())
    pygame.draw.rect(WINDOW, RED, red_rect)

    # Draw the green rectangle vertically
    green_rect = pygame.Rect(ship.x - 10, ship.y + SPACESHIP_IMAGE.get_height() - SPACESHIP_IMAGE.get_height() * (player_health / max_player_health), 10, SPACESHIP_IMAGE.get_height() * (player_health / max_player_health))
    pygame.draw.rect(WINDOW, GREEN, green_rect)
    pygame.display.update()
   
    

    #Draw second ships healthbar to screen
    # Draw the red rectangle vertically
    red_rect2 = pygame.Rect(second_ship.x - 10, second_ship.y, 10, BLUE_SPACESHIP_IMAGE.get_height())
    pygame.draw.rect(WINDOW, RED, red_rect2)

    # Draw the green rectangle vertically
    green_rect2 = pygame.Rect(second_ship.x - 10, second_ship.y + SPACESHIP_IMAGE.get_height() - SPACESHIP_IMAGE.get_height() * (second_player_health / max_player_health), 10, SPACESHIP_IMAGE.get_height() * (second_player_health / max_player_health))
    pygame.draw.rect(WINDOW, GREEN, green_rect2)
    pygame.display.update()


def Two_Player():
    lasers = []
    second_lasers = []
    ship = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    second_ship = pygame.Rect(100, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    ship = pygame.Rect(100, 200, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    top_enemy = None
    bottom_enemy = None
    enemy_lasers=[]
    game_mode = 0
    enemies = []
    clock = pygame.time.Clock()
    run = True
    global lost,player_health,wave,highest_wave,second_player_health
    lost = False
    first_wave = True
    power_up = None
    player_health = 15
    second_player_health = 15
    shot_probability = 0.001
    start_time = 0
    start_time_2 = 0
    wave = 0
    max_lasers = 3 
    second_max_lasers= 3
    while run:
        clock.tick(FPS)
        # check if all enemies are dead
        if len(enemies) == 0:
            # choose a new game mode randomly
            game_mode = random.randint(1, 2)
            enemies, top_enemy, bottom_enemy = generate_enemies(game_mode)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Check for timer event to restore max lasers
    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    Pause()  

                if event.key == pygame.K_SPACE and len(lasers)<max_lasers:
                    laser = pygame.Rect(
                        ship.x + SPACESHIP_WIDTH,
                        ship.y + SPACESHIP_HEIGHT // 2 - 2,
                        10,
                        5,
                    )
                    lasers.append(laser)
                if event.key == pygame.K_RETURN and len(second_lasers)<second_max_lasers:
                    laser = pygame.Rect(
                        second_ship.x + SPACESHIP_WIDTH,
                        second_ship.y + SPACESHIP_HEIGHT // 2 - 2,
                        10,
                        5,
                    )
                    second_lasers.append(laser)

        pressed_keys = pygame.key.get_pressed()
        ship_movement(pressed_keys, ship)
        second_ship_movement(pressed_keys,second_ship)

        for enemy in enemies:
            if game_mode==1:
                enemy.update()
                if random.random() < shot_probability:  # adjust the probability of shooting
                    enemy.shoot(enemy_lasers)
        handle_lasers_two_player(ship,second_ship,lasers,enemies)
        handle_lasers_two_player(ship,second_ship,second_lasers,enemies)
        handle_lasers_two_player(ship,second_ship,enemy_lasers,enemies, is_enemy=True)
        # update enemies
        if game_mode ==1:
            for enemy in enemies:
                enemy.update()
                if enemy.rect.y < top_enemy.rect.y:
                    top_enemy = enemy
                elif enemy.rect.y > bottom_enemy.rect.y:
                    bottom_enemy = enemy
        else:
            pass
        # check if top or bottom enemy has reached the screen edge
        if game_mode == 1 and top_enemy and bottom_enemy:
            if top_enemy.rect.top <= 0 or bottom_enemy.rect.bottom >= HEIGHT:
                for enemy in enemies:
                    enemy.direction *= -1
        else:
            pass

        if game_mode ==2:
            for enemy in enemies:
                enemy.move()

                if random.random() < shot_probability:
                    enemy.shoot(enemy_lasers)
                if enemy.get_x_coord()+ enemy_img.get_width()<0:
                    enemies.remove(enemy)
                    player_health -=0.5
                    second_player_health-=0.5

        #creaeta pwer up
        global powerup_on_screen
        if powerup_on_screen:
            power_up.should_disappear()
            power_up.collide(ship)
            power_up.collide(second_ship)
            
            
            if power_up.collected or power_up.expired:
                powerup_on_screen = False
        else:
        # spawn a new power-up
            if random.random() < 0.0005:
                power_up = PowerUp(random.randrange(0,200), random.randrange(50, HEIGHT-50),
                                    powerup_img.get_width(), powerup_img.get_height(), powerup_img)
                powerup_on_screen = True
        
        # Handle power-up for player one
        if power_up:
           if power_up.rect.colliderect(ship):
        # Power-up collected, set max lasers to 6
                max_lasers = 6
                start_time = time.time()
        if( time.time() - start_time)>=5:
            max_lasers = 3

        # Handle power-up for player two
        if power_up:
           if power_up.rect.colliderect(second_ship):
        # Power-up collected, set max lasers to 6
                second_max_lasers = 6
                start_time_2 = time.time()
        if( time.time() - start_time_2)>=5:
            second_max_lasers = 3
        TWO_PLAYER_DRAW_WINDOW(ship,second_ship, lasers,second_lasers, enemies, enemy_lasers,power_up)
        if player_health <=0:
            WINDOW.blit(GAME_OVER_IMAGE,(WIDTH//2 - GAME_OVER_IMAGE.get_width()//2,HEIGHT//2 - GAME_OVER_IMAGE.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            winner_text = FONT.render("PLAYER 2 WINS!",False, RED)
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            WINDOW.blit(winner_text, winner_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
        if second_player_health<=0:
            WINDOW.blit(GAME_OVER_IMAGE,(WIDTH//2 - GAME_OVER_IMAGE.get_width()//2,HEIGHT//2 - GAME_OVER_IMAGE.get_height()//2))
            pygame.display.update()
            pygame.time.delay(1000)
            winner_text = FONT.render("PLAYER 1 WINS!",False, RED)
            winner_rect = winner_text.get_rect(center=(WIDTH // 2, HEIGHT - 100))
            WINDOW.blit(winner_text, winner_rect)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False
        if len(enemies) == 0 or first_wave:
            # Increment the wave counter
            wave += 1
            #Increment the shot probability and wavelength to increase game difficulty
            global wavelength
            wavelength += 0.5
            shot_probability += 0.0001
            # Display the wave number
            wave_text = FONT.render(f"Wave {wave}",False, WHITE)
            wave_rect = wave_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WINDOW.blit(wave_text, wave_rect)
            pygame.display.update()
            pygame.time.delay(2000)  
            lasers.clear()
            first_wave = False

        pygame.display.update()
main_menu()