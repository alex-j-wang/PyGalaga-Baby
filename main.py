import pygame

pygame.init()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

def main():
	screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT :
				run = False
		pygame.display.update()
	pygame.quit()

main()



