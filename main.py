import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Plane and tower dimensions (based on percentages)
PLANE_WIDTH = int(SCREEN_WIDTH * 0.13)  # Plane width is 20% of screen width
PLANE_HEIGHT = int(SCREEN_HEIGHT * 0.1)  # Plane height is 10% of screen height
TOWER_WIDTH = int(SCREEN_WIDTH * 0.2)  # Tower width is 12% of screen width
TOWER_HEIGHT = int(SCREEN_HEIGHT * 0.15)  # Tower height is 15% of screen height
FLAG_WIDTH = int(SCREEN_WIDTH * 0.08)  # Flag width is 10% of screen width
FLAG_HEIGHT = int(SCREEN_HEIGHT * 0.11)  # Flag height is 8% of screen height

class Plane:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLANE_WIDTH
        self.height = PLANE_HEIGHT
        self.image = pygame.image.load('plane.png')  # Load plane image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Resize image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, keys):
        """Move the plane horizontally based on key presses."""
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= 5
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += 5

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Draw the plane on the screen."""
        screen.blit(self.image, self.rect)

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TOWER_WIDTH
        self.height = TOWER_HEIGHT
        self.image = pygame.image.load('tower.png')  # Load tower image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Resize image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, speed):
        """Move the tower downwards."""
        self.y += speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Draw the tower on the screen."""
        screen.blit(self.image, self.rect)

class AmericanFlag:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = FLAG_WIDTH
        self.height = FLAG_HEIGHT
        self.image = pygame.image.load('america.png')  # Load American flag image
        self.image = pygame.transform.scale(self.image, (self.width, self.height))  # Resize image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self, speed):
        """Move the flag downwards."""
        self.y += speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        """Draw the flag on the screen."""
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Plane Collection Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.plane = Plane(SCREEN_WIDTH // 2 - PLANE_WIDTH // 2, SCREEN_HEIGHT - PLANE_HEIGHT - 10)
        self.towers = []
        self.flags = []  # List to store flags
        self.tower_speed = 5
        self.score = 0
        self.background = pygame.image.load('background.png')  # Load background image
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Resize to screen size

    def spawn_tower(self):
        """Randomly spawn a tower at the top of the screen, but only if there are less than 3 towers on screen."""
        if len(self.towers) < 3:  # Only spawn if there are less than 3 towers
            x = random.randint(0, SCREEN_WIDTH - TOWER_WIDTH)
            tower = Tower(x, -TOWER_HEIGHT)  # Start above the screen
            self.towers.append(tower)

    def spawn_flag(self):
        """Randomly spawn an American flag with 0.5% chance every frame."""
        if random.random() < 0.005:  # 0.5% chance to spawn a flag
            x = random.randint(0, SCREEN_WIDTH - FLAG_WIDTH)
            flag = AmericanFlag(x, -FLAG_HEIGHT)  # Start above the screen
            self.flags.append(flag)

    def check_collection(self):
        """Check if the plane has passed (collected) any tower or flag."""
        collected_towers = []
        collected_flags = []

        # Check for tower collection
        for tower in self.towers:
            if self.plane.rect.colliderect(tower.rect):
                collected_towers.append(tower)
                self.score += 1  # Increase score when collecting a tower

        # Check for flag collection
        for flag in self.flags:
            if self.plane.rect.colliderect(flag.rect):
                collected_flags.append(flag)
                self.score -= 1  # Decrease score when collecting an American flag

        return collected_towers, collected_flags

    def update(self):
        """Update game elements."""
        keys = pygame.key.get_pressed()
        self.plane.move(keys)

        # Move towers and flags down
        for tower in self.towers:
            tower.move(self.tower_speed)
        for flag in self.flags:
            flag.move(self.tower_speed)

        # Remove collected towers and flags
        collected_towers, collected_flags = self.check_collection()
        for tower in collected_towers:
            self.towers.remove(tower)
        for flag in collected_flags:
            self.flags.remove(flag)

        # Remove towers and flags that are off-screen (bottom of screen)
        self.towers = [tower for tower in self.towers if tower.y < SCREEN_HEIGHT]
        self.flags = [flag for flag in self.flags if flag.y < SCREEN_HEIGHT]

        # Spawn new towers randomly (with 2% chance)
        if random.random() < 0.02:  # 2% chance to spawn a tower each frame
            self.spawn_tower()

        # Spawn an American flag with 0.5% chance every frame
        self.spawn_flag()

    def draw(self):
        """Draw everything on the screen."""
        self.screen.blit(self.background, (0, 0))  # Draw background
        self.plane.draw(self.screen)

        for tower in self.towers:
            tower.draw(self.screen)
        for flag in self.flags:
            flag.draw(self.screen)

        # Display the score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {int(self.score)}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))

        pygame.display.update()

    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Handle user inputs and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()
