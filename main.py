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
	fps = 60
	game = Game()
	pygame.init()

	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	player = pygame.Rect((187, 500, 25, 50))


	run = True
	while run:
		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, (255, 0, 0), player)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		game.tick()

		key = pygame.key.get_pressed()
		key_event(key, player)
	
		pygame.display.update()
		clock.tick(fps)
	pygame.quit()

if __name__ == "__main__":
    main()