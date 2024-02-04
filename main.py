from logic import *
import pygame
import sys

from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
bullet_cooldown = 0 # Time in milliseconds between consecutive bullet spawns
pygame.mixer.init()
kill_sound = pygame.mixer.Sound('resources/kill.wav')
start_sound = pygame.mixer.Sound('resources/start.wav')
damage_sound = pygame.mixer.Sound('resources/damage.wav')

def key_event(key, player, bullets, last_bullet_time, can_fire):
	"""
	key_event is our key handler, allows you to control your rocket with 'a' and 'd' or arrow keys
	returns the last time you fired a bullet
	"""
	global bullet_cooldown
	current_time = pygame.time.get_ticks()

	if key[pygame.K_a] or key[pygame.K_LEFT]: # Allows you to move left when pushing a or left arrow
		player.move(False)
	elif key[pygame.K_d] or key[pygame.K_RIGHT]: # Allows you to move right when pushing d or right arrow
		player.move(True)
	if key[pygame.K_RETURN] or key[pygame.K_SPACE]: # Check if the ENTER or SPACE key is pressed 
		if can_fire: # Checks if you can fire or if you're still on cool down
			bullets.append(pygame.Rect(*player.center, 5, 10)) # Makes a bullet
			last_bullet_time = current_time # Update the last bullet time
			bullet_cooldown = 250 # Resets bullet cooldown
			
	return last_bullet_time # Returns the last time you shot

def shooting(bullets, game, screen, player, current_time, last_bullet_time):
	"""
	Contains all of our information on firing the weapon, returns the last time you fired
	Additionally checks if keys are pressed
	"""
	key = pygame.key.get_pressed() # Get keys that are pressed

	# Check if you can fire the bullet given the cool down time
	time_since_last_bullet =  current_time - last_bullet_time
	if (time_since_last_bullet >= bullet_cooldown):
		can_fire = True
	else:
		can_fire = False

	# Calls the key handler to handle all key events and shoot if return button is pressed
	last_bullet_time = key_event(key, player, bullets, last_bullet_time, can_fire)
	
	# Draws all of the bullets on screen
	for bullet in bullets:
		pygame.draw.rect(screen, (255, 255, 204), bullet, border_radius=2) # Draw bullets

	# Check collision between bullets and enemies
	for bullet in bullets:
		for enemy in game.enemies: # Same here
			if collides(bullet, pygame.Rect(enemy.x, enemy.y, 25, 25)):
				bullets.remove(bullet)
				game.enemies.remove(enemy)
				pygame.mixer.Sound.play(kill_sound)
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
	font = pygame.font.Font('freesansbold.ttf', 32) # Font for the game over text
	
	#checks if you won or lost
	if player.lives > 0:
		txt = "You Won!"
	else:
		txt = "You Lost!"

	#label holding the game over text
	label = font.render(txt, False, (255, 255, 255)) 
	label_rect = label.get_rect()
	label_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 15)

	# Loop that holds the game over loop
	run = True
	while run:
		for event in pygame.event.get(): #gets all of the events that occurs
			if event.type == QUIT: #closes window if you hit close
				run = False
		screen.blit(label, label_rect) # Puts the game over label on screen
		pygame.display.update()
	pygame.quit()

def main():
	"""
	Initializes several of our variables that we will need throughout our program
	such as screen and player
	"""
	pygame.init() # Initializes pygame
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Initializes the screen
	clock = pygame.time.Clock() # Initializes the clock to control fps
	
	pygame.display.set_caption("PyGalaga") # Titles the window 'Galaga'

	# Makes a background
	bg = pygame.image.load("resources/background.png").convert() 
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2

	# Loads in the heart images to denote lives left
	heart = pygame.image.load("resources/heart.png").convert()
	heart = pygame.transform.scale(heart, (15, 15))

	player = Player(screen) # Creates a player
	pygame.mixer.Sound.play(start_sound) # Plays the start sound
	loop(clock, screen, player, bg, tiles, heart) # Runs our loop that controls gameplay

def screen_update(tiles, screen, bg, scroll, game, player, heart):
	"""
	updates the screen with everything occuring
	"""
	font = pygame.font.Font('freesansbold.ttf', 16) # Font used for the level in the top left corner

	# Puts the background in
	for i in range(tiles):
		screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
	
	# Shows the title screen if it's level 0
	if (game.level == 0):
		title = pygame.font.Font('freesansbold.ttf', 32).render("PYGALAGA", False, (255, 255, 255))
		title_label = title.get_rect()
		title_label.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 15)
		screen.blit(title, title_label)

	# Shows the level and lives left with heart
	else:
		# Shows lives left
		for i in range(player.lives):
			screen.blit(heart, (15 * i + 20, 45))

		# Shows level
		level = font.render("Level: " + str(game.level), False, (255, 255, 255))
		level_label = level.get_rect()
		level_label.center = (50, 30)
		screen.blit(level, level_label)

	game.display_enemies(screen) #updates enemy position
	player.update(screen) # Updates player position

def loop(clock, screen, player, bg, tiles, heart):
	"""
	creates a game loop that controls game play
	"""
	game, scroll, run, can_fire, fps, last_bullet_time, quit = Game(), 0, True, True, 40, 0, False # Initializes a bunch of variables to use
	bullets = [] # List to store bullet rectangles

	while run:
		clock.tick(fps) # Runs the game at the given fps
		
		# Causes the infinite scrolling of the background
		scroll -= 5
		if abs(scroll) > bg.get_height():
			scroll = 0

		for enemy in game.enemies:
			if collides(player.rect, pygame.Rect(enemy.x, enemy.y, 25, 25)):
				game.enemies.remove(enemy)
				player.lives -= 1
				pygame.mixer.Sound.play(damage_sound)

		run = player.lives > 0 and game.tick(player) # Runs levels and enemies, checks if you have died

		# Allows you to click the quit button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
				run = False

		# Runs all of the shooting animation stuff and stores the last time a bullet was fired
		screen_update(tiles, screen, bg, scroll, game, player, heart) # Updates the screen
		last_bullet_time = shooting(bullets, game, screen, player, pygame.time.get_ticks(), last_bullet_time) 

		pygame.display.update()

	# If the user quit out of the game then quits and ends program
	if quit:
		pygame.quit()
		sys.exit()

	# Clears the screen
	for i in range(tiles):
		screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
	game_over(screen, player) # Runs game over sequence
	
	pygame.quit()

if __name__ == "__main__":
    main()