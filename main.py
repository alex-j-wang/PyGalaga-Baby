from logic import *
import pygame

from pygame.locals import *


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def key_event(key, player):
	if key[pygame.K_a]:
		player.move_ip(-1, 0)
	elif key[pygame.K_d]:
		player.move_ip(1, 0)


def main():
<<<<<<< Updated upstream
	
	game = Game()
=======
	pygame.init()
>>>>>>> Stashed changes
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
	player = pygame.Rect((187, 500, 25, 50))


	run = True
	#run = True
	while run:
		screen.fill((0, 0, 0))
		pygame.draw.rect(screen, (255, 0, 0), player)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
<<<<<<< Updated upstream
		game.tick()
=======
		key = pygame.key.get_pressed()
		key_event(key, player)
			#if event.type == pygame.KEYDOWN:
			#	if event.key == pygame.K_a:
			#		player.move_ip(-1, 0)
>>>>>>> Stashed changes
		pygame.display.update()
	pygame.quit()

if __name__ == "__main__":
    main()