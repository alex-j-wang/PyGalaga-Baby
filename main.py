import logic
from logic import *
import pygame

from pygame.locals import *


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def key_event(key, player):
	if key[pygame.K_a]:
		player.move_ip(-5, 0)
	elif key[pygame.K_d]:
		player.move_ip(5, 0)


def main():
	clock = pygame.time.Clock();
	fps = 40
	game = Game()
	pygame.init()

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	pygame.display.set_caption("Galaga")

	bg = pygame.image.load("background.png").convert()
	bg_height = bg.get_height()
	tiles = math.ceil(SCREEN_HEIGHT / bg_height) + 2
	print(tiles)
	scroll = 0


	player = pygame.Rect((187, 500, 25, 50))

	run = True
	while run:
		clock.tick(fps)
		for i in range(tiles):
			screen.blit(bg, (0, SCREEN_HEIGHT - (i * bg_height) - scroll))
			#print(i * bg_height - scroll)
		scroll -= 5
		if abs(scroll) > bg_height:
			scroll = 0

		pygame.draw.rect(screen, (255, 0, 0), player)
		game.display_enemies(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		game.tick()

		key = pygame.key.get_pressed()
		key_event(key, player)

		pygame.display.update()
		
	pygame.quit()

if __name__ == "__main__":
    main()

