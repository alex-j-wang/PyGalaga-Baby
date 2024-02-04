from logic import *
import pygame
import sys

from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
bullet_cooldown = 0 # Time in milliseconds between consecutive bullet spawns

def key_event(key, player, bullets, last_bullet_time, can_fire):
	"""
	key_event is our key handler, allows you to control your rocket with 'a' and 'd' or arrow keys
	returns the last time you fired a bullet
	"""
	global bullet_cooldown
	current_time = pygame.time.get_ticks()

	if key[pygame.K_a] or key[pygame.K_LEFT]: # allows you to move left when pushing a or left arrow
		player.move(False)
	elif key[pygame.K_d] or key[pygame.K_RIGHT]: # allows you to move right when pushing d or right arrow
		player.move(True)
	if key[pygame.K_RETURN]: # Check if the ENTER key is pressed 
		if can_fire: # checks if you can fire or if you're still on cool down
			bullets.append(pygame.Rect(player.center[0], player.center[1], 5, 10)) # makes a bullet
			last_bullet_time = current_time # Update the last bullet time
			bullet_cooldown = 250 # resets bullet cooldwon
			
	return last_bullet_time # returns the last time you shot

def shooting(bullets, game, screen, player, current_time, last_bullet_time):
	"""
	Contains all of our information on firing the weapon, returns the last time you fired
	Additionally checks if keys are pressed
	"""
	key = pygame.key.get_pressed() # get keys that are pressed

	# Check if you can fire the bullet given the cool down time
	time_since_last_bullet =  current_time - last_bullet_time
	if (time_since_last_bullet >= bullet_cooldown):
		can_fire = True
	else:
		can_fire = False

	# calls the key handler to handle all key events and shoot if return button is pressed
	last_bullet_time = key_event(key, player, bullets, last_bullet_time, can_fire)
	
	# draws all of the bullets on screen
	for bullet in bullets:
			pygame.draw.rect(screen, (255, 255, 255), bullet, border_radius=2) # Draw bullets

	# Check collision between bullets and enemies
	for bullet in bullets:
			for enemy in game.enemies: # Same here
				if collides(bullet, pygame.Rect(enemy.x, enemy.y, 25, 25)):
					bullets.remove(bullet)
					game.enemies.remove(enemy)
					break

	# Update bullet positions
	for bullet in bullets:
			bullet.move_ip(0, -10) # Adjust the bullet speed as needed
	# Remove bullets that have gone off-screen
	bullets = [bullet for bullet in bullets if bullet.y > 0]
	return last_bullet_time

def game_over(screen, player):
	"""
	performs game over sequence if the game is over, called at the end of the main loop
	"""
	font = pygame.font.Font('freesansbold.ttf', 32) # font for the game over text
	
	#checks if you won or lost
	if player.lives > 0:
		txt = "You Won!"
	else:
		txt = "You Lost!"

	#label holding the game over text
	label = font.render(txt, False, (255, 255, 255)) 
	label_rect = label.get_rect()
	label_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 15)

	# loop that holds the game over loop
	run = True
	while run:
		for event in pygame.event.get(): #gets all of the events that occurs
			if event.type == QUIT: #closes window if you hit close
				run = False
		screen.blit(label, label_rect) # puts the game over label on screen
		pygame.display.update()
	pygame.quit()

def main():
	"""
	Initializes several of our variables that we will need throughout our program
	such as screen and player
	"""
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # initializes the screen
	clock = pygame.time.Clock() # initializes the clock to control fps
	
	pygame.display.set_caption("Galaga") # titles the window 'Galaga'

	# makes a background
	bg = pygame.image.load("background.png").convert() 
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2

	# loads in the heart images to denote lives left
	heart = pygame.image.load("heart.png").convert()
	heart = pygame.transform.scale(heart, (15, 15))

	player = Player(screen) # creates a player
	
	loop(clock, screen, player, bg, tiles, heart) # runs our loop that controls gameplay

def screen_update(tiles, screen, bg, scroll, game, player, heart):
	"""
	updates the screen with everything occuring
	"""
	font = pygame.font.Font('freesansbold.ttf', 16) # font used for the level in the top left corner

	# puts the background in
	for i in range(tiles):
		screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
	
	# shows the title screen if it's level 0
	if (game.level == 0):
		title = pygame.font.Font('freesansbold.ttf', 32).render("GALAGA", False, (255, 255, 255))
		title_label = title.get_rect()
		title_label.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 15)
		screen.blit(title, title_label)

	# shows the level and lives left with heart
	else:
		# shows lives left
		for i in range(player.lives):
			screen.blit(heart, (15 * i + 20, 45))

		# shows level
		level = font.render("Level: " + str(game.level), False, (255, 255, 255))
		level_label = level.get_rect()
		level_label.center = (50, 30)
		screen.blit(level, level_label)

	game.display_enemies(screen) #updates enemy position
	player.update(screen) # updates player position
	

def loop(clock, screen, player, bg, tiles, heart):
	"""
	creates a game loop that controls game play
	"""
	game, scroll, run, can_fire, fps, last_bullet_time, quit = Game(), 0, True, True, 40, 0, False # initializes a bunch of variables to use
	bullets = [] # List to store bullet rectangles

	while run:
		clock.tick(fps) # runs the game at the given fps
		
		# causes the infinite scrolling of the background
		scroll -= 5
		if abs(scroll) > bg.get_height():
			scroll = 0

		for enemy in game.enemies:
			if collides(player.rect, pygame.Rect(enemy.x, enemy.y, 25, 25)):
				game.enemies.remove(enemy)
				player.lives -= 1

		run = player.lives > 0 and game.tick(player) # runs levels and enemies, checks if you have died

		# Allows you to click the quit button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
				run = False

		# runs all of the shooting animation stuff and stores the last time a bullet was fired
		screen_update(tiles, screen, bg, scroll, game, player, heart) # updates the screen
		last_bullet_time = shooting(bullets, game, screen, player, pygame.time.get_ticks(), last_bullet_time) 

		pygame.display.update()

	# if the user quit out of the game then quits and ends program
	if quit:
		pygame.quit()
		sys.exit()

	# clears the screen
	for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
	game_over(screen, player) # runs game over sequence
	
	pygame.quit()

if __name__ == "__main__":
    main()