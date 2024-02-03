# IDEAS
# sandbox mode
# multiplayer?
# more fighter abilities

class Enemy:
    def __init__(self, name, health, x, y):
        self.name = name
        self.health = health
        self.x = x
        self.y = y

class Player:
    def __init__(self):
        self.health = 3
        self.x = 50 # may need to be updated
        self.y = 10 # may need to be updated

def main():
    player = Player()

if __name__ == "__main__":
    main()