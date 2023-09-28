'''
Author: Yifan Gong
Date: 28 Sep 2023
'''


from resources import *
from Data import *
from slider import *
from palette import *
from rails import *

# Initialize
pygame.init()
time = 0
COUNT = 7
counter = COUNT


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if KNOB_X <= event.pos[0] <= KNOB_X + KNOB_WIDTH and KNOB_Y <= event.pos[1] <= KNOB_Y + KNOB_HEIGHT:
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            KNOB_X = event.pos[0] - KNOB_WIDTH // 2
            KNOB_X = max(SLIDER_X, min(KNOB_X, SLIDER_X + SLIDER_WIDTH - KNOB_WIDTH))

    # Clear the screen with a color (optional, but can help with visual artifacts)
    screen.fill(WHITE)

    # Update the colour list
    # Colour list with a given time is a list of (time / TIME_INTERVAL)th item in each list in the capacity_list
    # Only change colour when the counter is COUNT
    if counter == COUNT:
        colour_list = []
        for idx in range(len(polygons)):
            colour_list.append(colour(capacity_list[idx]))

        # update capacity_list
        capacity_list = update_capacity_list(capacity_list)

    i = 0
    # Draw the polygons
    for polygon_points in polygons:
        pygame.draw.polygon(screen, colour_list[i], polygon_points)
        i += 1

    # Blit the image onto the screen
    screen.blit(background_image, (0, 0))

    # Running of the trains
    for i in range(len(railways)):
        # Running of the trains from city
        train_pos_reverse = train_position_reverse(railways[i], dist_traveled_reverse_list[i])
        pygame.draw.circle(screen, EMPTY_TRAIN, train_pos_reverse, 10)

        dist_traveled_reverse_list[i] += SPEED
        dist_traveled_reverse_list[i] %= track_length_reverse_list[i]

        # Running of the trains towards city
        train_pos = train_position(railways[i], dist_traveled_list[i])
        pygame.draw.circle(screen, FULL_TRAIN, train_pos, 10)

        dist_traveled_list[i] += SPEED
        dist_traveled_list[i] %= track_length_list[i]

    # Draw slider bar
    pygame.draw.rect(screen, SLIDER_COLOUR, (SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT))

    # Draw slider knob
    pygame.draw.rect(screen, KNOB_COLOUR, (KNOB_X, KNOB_Y, KNOB_WIDTH, KNOB_HEIGHT))

    # Calculate the hour value based on the knob's position
    pct = (KNOB_X - SLIDER_X) / (SLIDER_WIDTH - KNOB_WIDTH)
    time = round(pct * 24, 1)

    # Adjust hours to the nearest 0.25 increment
    time = round(time * 4) / 4
    time += 0.25 if counter == 0 else 0
    counter = COUNT if counter == 0 else counter - 1
    time %= 24

    # Adjust knob's position based on the adjusted hours
    KNOB_X = SLIDER_X + (time / 24) * (SLIDER_WIDTH - KNOB_WIDTH)

    # Draw the icons
    screen.blit(wind_icon, (185, 14))
    screen.blit(solar_icon, (501, 11))
    screen.blit(hydro_icon, (801, 7))

    # Update display
    pygame.display.flip()

pygame.quit()
