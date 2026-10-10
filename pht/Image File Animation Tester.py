import pygame as pg
import sys

pg.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 10  # Adjust this to control the speed of the "animation"

# Colors
WHITE = (255, 255, 255)

# List of image paths
image_paths = ["pht1.png", "pht2.png","pht3.png", "pht4.png", "pht5.png","pht6.png", "pht7.png", "pht8.png","pht9.png","pht10.png", "pht11.png","pht12.png","pht13.png", "pht14.png", "pht15.png"]
images = [pg.image.load(img_path) for img_path in image_paths]

# Initialize screen and clock
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Image Viewer")
clock = pg.time.Clock()

current_image = 0

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # Optionally add controls to go to next or previous image using keyboard arrows
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                current_image = (current_image + 1) % len(images)
            elif event.key == pg.K_LEFT:
                current_image = (current_image - 1) % len(images)

    screen.fill(0)
    # Get the current image and its dimensions
    image = images[current_image]
    img_width, img_height = image.get_size()

    # Draw the current image at the center of the screen
    screen.blit(image, ((SCREEN_WIDTH - img_width) // 2, (SCREEN_HEIGHT - img_height) // 2))

    pg.display.flip()
    clock.tick(FPS)
