from logic import *
import pygame
import sys

from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
bullet_cooldown = 0  # Time in milliseconds between consecutive bullet spawns

def key_event(key, player, bullets, last_bullet_time, can_fire):
	global bullet_cooldown
	current_time = pygame.time.get_ticks()

	if key[pygame.K_a] or key[pygame.K_LEFT]:
		player.move(False)
	elif key[pygame.K_d] or key[pygame.K_RIGHT]:
		player.move(True)
	if key[pygame.K_RETURN]:  # Check if the ENTER key is pressed
		if can_fire:
			bullets.append(pygame.Rect(player.center[0], player.center[1], 5, 10))
			last_bullet_time = current_time  # Update the last bullet time
			bullet_cooldown = 250

	return last_bullet_time

def shooting(bullets, game, screen):
	for bullet in bullets:
			pygame.draw.rect(screen, (255, 255, 255), bullet, border_radius=2)  # Draw bullets

	# Check collision between bullets and enemies
	for bullet in bullets:
			for enemy in game.enemies:  # Same here
				if collides(bullet, pygame.Rect(enemy.x, enemy.y, 25, 25)):
					bullets.remove(bullet)
					game.enemies.remove(enemy)
					break

		# Update bullet positions
	for bullet in bullets:
			bullet.move_ip(0, -10)  # Adjust the bullet speed as needed
		# Remove bullets that have gone off-screen
	bullets = [bullet for bullet in bullets if bullet.y > 0]

def game_over(won, screen):
	font = pygame.font.Font('freesansbold.ttf', 32)
	if won:
		txt = "You Won!"
	else:
		txt = "You Lost!"
	label = font.render(txt, False, (255,255,255)) 
	label_rect = label.get_rect()
	label_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 15)
	run = True
	while run:
		for event in pygame.event.get(): #gets all of the events that occurs
			if event.type == QUIT: #closes window if you hit close
				run = False
		screen.blit(label, label_rect)
		pygame.display.update()
	pygame.quit()

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock()
	
	pygame.display.set_caption("Galaga")

	bg = pygame.image.load("background.png").convert()
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2

	heart = pygame.image.load("heart.png").convert()
	heart = pygame.transform.scale(heart, (15, 15))

	player = Player(screen)
	
	loop(clock, screen, player, bg, tiles, heart)

def loop(clock, screen, player, bg, tiles, heart):
	game, scroll, run, can_fire, fps, last_bullet_time, quit = Game(), 0, True, True, 40, 0, False
	bullets = []  # List to store bullet rectangles
	font = pygame.font.Font('freesansbold.ttf', 16)
	while run:
		
		clock.tick(fps)
		for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
		scroll -= 5
		if abs(scroll) > bg.get_height():
			scroll = 0

		game.display_enemies(screen)

		shooting(bullets, game, screen)

		for enemy in game.enemies:
			if collides(player.rect, pygame.Rect(enemy.x, enemy.y, 25, 25)):
				game.enemies.remove(enemy)
				player.lives -= 1

		run = player.lives > 0 and game.tick()

		# Allows you to click the quit button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
				run = False

		key = pygame.key.get_pressed()

		time_since_last_bullet = pygame.time.get_ticks() - last_bullet_time
		if (time_since_last_bullet >= bullet_cooldown):
			can_fire = True
		else:
			can_fire = False

		last_bullet_time = key_event(key, player, bullets, last_bullet_time, can_fire)

		#key_event(key, player)
		player.update(screen)

		for i in range(player.lives):
			screen.blit(heart, (15 * i + 20, 45))

		level = font.render("Level: " + str(game.level), False, (255, 255, 255))
		level_label = level.get_rect()
		level_label.center = (50, 30)
		screen.blit(level, level_label)

		pygame.display.update()

	if quit:
		pygame.quit()
		sys.exit()

	if player.lives > 0:
		win = True
	else:
		win = False
	for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
	game_over(win, screen)
	
	pygame.quit()

if __name__ == "__main__":
    main()