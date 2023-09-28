import pygame

# Load image
image_path = "src/mapOnlyRoadBlackTracex0.5.png"
background_image = pygame.image.load(image_path)

# Set the window size to the image size
screen_width, screen_height = background_image.get_size()
screen = pygame.display.set_mode((screen_width, screen_height))


# icons
icon_size = (70, 70)  # 用您希望的宽度和高度替换这个值

wind_icon = pygame.image.load('src/windIcon.png')
solar_icon = pygame.image.load('src/solarIcon.png')
hydro_icon = pygame.image.load('src/hydroIcon.png')

