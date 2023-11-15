# Import pre-installed libs.
import os
import platform
import random
import pygame
import math

# Create a clear function.
def clear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

# Create a function to install libs and pip.
def installer():
    if platform.system() == "Windows":
        os.system("py -m ensurepip --upgrade")
        os.system("py get-pip.py")
    else:
        os.system("python3 -m ensurepip --upgrade")
        os.system("pip install --upgrade pip")
        os.system("pip3 install --upgrade pip")
    os.system("pip install -r Requirements.txt")
    os.system("pip3 install -r Requirements.txt")
    clear()

try:
    from pygame.locals import QUIT
    from pygame.time import Clock
    from pygame.math import Vector3
    import imageio
except ImportError:
    installer()

# Create a function to save the animation.
def create_animation(output_path='output.mov'):
    pygame.init()

    # Set up Pygame window
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("3Oke")

    clock = Clock()

    # Set up animation for 3 minutes
    duration_seconds = 180
    frames_per_second = 30
    total_frames = duration_seconds * frames_per_second

    frames = []
    for frame_num in range(total_frames):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

        # Randomize background color
        background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        screen.fill(background_color)

        # Randomize object color
        object_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # Randomize object and its position
        object_size = random.randint(10, 50)
        object_position = Vector3(random.randint(0, width - object_size), random.randint(0, height - object_size), 0)

        # Randomize object shape (circle or rectangle)
        if random.choice([True, False]):
            # Draw a circle
            pygame.draw.circle(screen, object_color, (int(object_position.x + object_size / 2), int(object_position.y + object_size / 2)), int(object_size / 2))
        else:
            # Draw a rectangle
            pygame.draw.rect(screen, object_color, (object_position.x, object_position.y, object_size, object_size))

        pygame.display.flip()
        clock.tick(frames_per_second)

        # Capture frames for later saving as .mov
        frames.append(pygame.surfarray.array3d(screen))

    # Save frames as .mov file
    imageio.mimsave(output_path, frames, fps=frames_per_second)

if __name__ == "__main__":
    create_animation()
