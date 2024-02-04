from logic import *
import pygame

from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
bullet_cooldown = 0  # Time in milliseconds between consecutive bullet spawns

def key_event(key, player, bullets, last_bullet_time, can_fire):
	global bullet_cooldown
	current_time = pygame.time.get_ticks()

	if key[pygame.K_a]:
		player.move(False)
	elif key[pygame.K_d]:
		player.move(True)
	if key[pygame.K_RETURN]:  # Check if the ENTER key is pressed
		if can_fire:
			bullets.append(pygame.Rect(player.rect.centerx, player.rect.top, 5, 10))
			last_bullet_time = current_time  # Update the last bullet time
			bullet_cooldown = 250

	return last_bullet_time

def shooting(bullets, game, screen):
	for bullet in bullets:
			pygame.draw.rect(screen, (0, 255, 0), bullet)  # Draw bullets as green rectangles


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

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock();
	
	pygame.display.set_caption("Galaga")

	bg = pygame.image.load("background.png").convert()
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2

	player_image = pygame.image.load("rocket-removebg-preview.png").convert_alpha()
	player = Player(player_image)
	player.rect.x = 185
	player.rect.y = 500
	
	loop(clock, screen, player, bg, tiles)


def shooting(bullets, game, screen):
	for bullet in bullets:
		pygame.draw.rect(screen, (0, 255, 0), bullet)  # Draw bullets as green rectangles


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


def loop(clock, screen, player, bg, tiles):
	game, scroll, run, can_fire, fps, last_bullet_time = Game(), 0, True, True, 40, 0
	bullets = []  # List to store bullet rectangles
	while run:
		clock.tick(fps)
		for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg.get_height()) - scroll))
		scroll -= 5
		if abs(scroll) > bg.get_height():
			scroll = 0

		game.display_enemies(screen)

		shooting(bullets, game, screen)

		# Allows you to click the quit button
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		run = game.tick()

		key = pygame.key.get_pressed()

		time_since_last_bullet = pygame.time.get_ticks() - last_bullet_time
		if (time_since_last_bullet >= bullet_cooldown):
			can_fire = True
		else:
			can_fire = False

		last_bullet_time = key_event(key, player, bullets, last_bullet_time, can_fire)

		#key_event(key, player)
		player.update(screen)

		pygame.display.update()

	print('You win!')
	pygame.quit()

if __name__ == "__main__":
    main()