from logic import *
import pygame

from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BULLET_COOLDOWN = 0  # Time in milliseconds between consecutive bullet spawns


def key_event(key, player, bullets, last_bullet_time, can_fire):
	global BULLET_COOLDOWN
	current_time = pygame.time.get_ticks()

	if key[pygame.K_a]:
		player.move(False)
	elif key[pygame.K_d]:
		player.move(True)
	if key[pygame.K_RETURN]:  # Check if the ENTER key is pressed
		if can_fire:
			bullets.append(pygame.Rect(player.rect.centerx, player.rect.top, 5, 10))
			last_bullet_time = current_time  # Update the last bullet time
			BULLET_COOLDOWN = 250

	return last_bullet_time
	


	return last_bullet_time if key[pygame.K_RETURN] else current_time  # Return None if Enter is not pressed

def main():
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	clock = pygame.time.Clock();
	fps = 40
	game = Game()
	
	pygame.display.set_caption("Galaga")

	bg = pygame.image.load("background.png").convert()
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2
	
	scroll = 0


	bullets = []  # List to store bullet rectangles
	last_bullet_time = 0

	player_image = pygame.image.load("rocket-removebg-preview.png").convert_alpha()
	player = Player(player_image)
	player.rect.x = 185
	player.rect.y = 500
	can_fire = True
	run = True
	while run:
		clock.tick(fps)
		for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg_height) - scroll))
		scroll -= 5
		if abs(scroll) > bg_height:
			scroll = 0

		game.display_enemies(screen)

		for bullet in bullets:
			pygame.draw.rect(screen, (0, 255, 0), bullet)  # Draw bullets as green rectangles


	# Check collision between bullets and enemies
		for bullet in bullets:
			for enemy in game.enemies:  # Same here
				if collides(bullet, pygame.Rect(enemy.x, enemy.y, 25, 25)):
					bullets.remove(bullet)
					game.enemies.remove(enemy)
					break

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		game.tick()

		key = pygame.key.get_pressed()

		time_since_last_bullet = pygame.time.get_ticks() - last_bullet_time
		if (time_since_last_bullet >= BULLET_COOLDOWN):
			can_fire = True
		else:
			can_fire = False

		last_bullet_time = key_event(key, player, bullets, last_bullet_time, can_fire)

		# Update bullet positions
		for bullet in bullets:
			bullet.move_ip(0, -10)  # Adjust the bullet speed as needed
		# Remove bullets that have gone off-screen
		bullets = [bullet for bullet in bullets if bullet.y > 0]


		#key_event(key, player)
		player.update(screen)

		pygame.display.update()

	pygame.quit()

if __name__ == "__main__":
    main()