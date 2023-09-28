'''
Author: Ziqi Wang
Date: 28 Sep 2023
'''


import pygame
import sys
import palette

def load_image_scaled(image_path, scale_factor):
    # Load the image
    image = pygame.image.load(image_path)

    # Get the dimensions of the original image
    width, height = image.get_size()

    # Calculate the scaled dimensions
    scaled_width = int(width * scale_factor)
    scaled_height = int(height * scale_factor)

    # Scale the image
    scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))

    return scaled_image

# 初始化pygame
pygame.init()
# 设置参数
SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 1015
BACKGROUND_COLOR = (255, 255, 255)
SWITCH_GREEN = (0, 255, 0)
SWITCH_RED = (255, 0, 0)
CIRCLE_COLOR = (173, 216, 230)  # Light blue color
LINE_COLOR = (0, 0, 0)
PROGRESSBAR_Y = SCREEN_HEIGHT - 100
PROGRESSBAR_WIDTH = 600
PROGRESSBAR_HEIGHT = 20
PROGRESS_COLOR = (0, 255, 0)
PROGRESSBAR_X = (SCREEN_WIDTH - PROGRESSBAR_WIDTH) // 2

# Load image
image_path = "src/mapOnlyRoadBlackTracex0.5.png"
background_image = load_image_scaled(image_path, 1.5)
background_image.set_alpha(180)

dragging = False
coordinates = [(227, -1), (217, 88), (310, 136), (339, 193), (378, 198), (379, 209), (372, 263), (380, 291), (392, 315),
     (407, 342), (431, 358), (439, 374), (513, 449), (541, 522)]
times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # An example timeline
max_time = times[-1]-1

# 开关设置
SWITCH_WIDTH = 30
SWITCH_HEIGHT = 30
SWITCH_X = (SCREEN_WIDTH - 860)
SWITCH_Y = (SCREEN_HEIGHT - 105)
switch_status = False  # 默认关闭

# Train data: starting_time, battery_count, current_percentage
trains = [
    {"start_time": 0, "battery_count": 700, "percentage": 0},
    {"start_time": 2, "battery_count": 300, "percentage": 0},
    {"start_time": 4, "battery_count": 500, "percentage": 0},
    {"start_time": 6, "battery_count": 800, "percentage": 0},
    {"start_time": 8, "battery_count": 800, "percentage": 0},
    {"start_time": 10, "battery_count": 800, "percentage": 0},
    {"start_time": 12, "battery_count": 700, "percentage": 0},
]
battery_warehouses = [
    {"position": coord, "battery_count": 10} for coord in coordinates[1:]
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def get_train_position(percentage):
    time = percentage * max_time
    for i in range(len(times) - 1):
        if times[i] <= time <= times[i + 1]:
            alpha = (time - times[i]) / (times[i + 1] - times[i])
            start_x, start_y = coordinates[i]
            end_x, end_y = coordinates[i + 1]
            x_position = (1 - alpha) * start_x + alpha * end_x
            y_position = (1 - alpha) * start_y + alpha * end_y
            return x_position*1.5, y_position*1.5  # We scale the coordinates for better visualization
    return -1, -1  # Outside of the defined time range


def draw_train(x, y, battery_count):
    pygame.draw.circle(screen, CIRCLE_COLOR, (int(x), int(y)), battery_count/20)

    # Add the battery count in the center of the circle
    font = pygame.font.SysFont(None, 25)
    text_surface = font.render("{:.2f}".format(battery_count), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(int(x), int(y)))
    screen.blit(text_surface, text_rect)


def update_battery_warehouses(train_percentage, train):
    tolerance = 50
    for warehouse in battery_warehouses:
        x, y = warehouse["position"]
        x = x*1.5
        y = y*1.5
        train_x, train_y = get_train_position(train_percentage)

        distance = ((train_x - x) ** 2 + (train_y - y) ** 2) ** 0.5
        if warehouse["position"][0] < 431:
            if distance < tolerance and warehouse["battery_count"] < 10:
                if train["battery_count"] >= 25 - warehouse["battery_count"]:
                    train["battery_count"] = train["battery_count"] - (25 - warehouse["battery_count"])
                    warehouse["battery_count"] = 25
                else:
                    warehouse["battery_count"] = warehouse["battery_count"] + train["battery_count"]
                    train["battery_count"] = 0
        else:
            if distance < tolerance and warehouse["battery_count"] < 80:
                if train["battery_count"]>=110-warehouse["battery_count"]:
                    train["battery_count"] =train["battery_count"]-(110-warehouse["battery_count"])
                    warehouse["battery_count"] = 110
                else:
                    warehouse["battery_count"]=warehouse["battery_count"]+train["battery_count"]
                    train["battery_count"]=0

def lerp(a, b, t):
        """Linear interpolation between a and b."""
        return a + t * (b - a)


def get_color_for_battery(battery_count):
    if battery_count <= 0:
        t = -battery_count / 50.0  # Map the range [-50, 0] to [0, 1]
        c = palette.blend_colors(t, palette.ZERO_CAPACITY_COLOUR, palette.FULL_CAPACITY_COLOUR)
    elif battery_count <= 70:
        t = battery_count / 70.0  # Map the range [0, 70] to [0, 1]
        c = palette.blend_colors(t, palette.FULL_CAPACITY_COLOUR, (64, 146, 201))
    else:
        c = (64, 146, 201)  # Just blue for counts above 70

    return c


def draw_battery_warehouses():
    for warehouse in battery_warehouses:
        x, y = warehouse["position"]
        x=x*1.5
        y=y*1.5
        color = get_color_for_battery(warehouse["battery_count"])
        pygame.draw.rect(screen, color, (x-10, y-10, 20, 20))  # Draw a yellow square below the coordinate point

        pygame.draw.rect(screen, (238, 229, 233), (x + 20, y - 10, 50, 20))  # Draw a yellow square below the coordinate point

        font = pygame.font.SysFont(None, 24)
        text = font.render("{:.2f}".format(warehouse["battery_count"]), True, (56, 61, 59))
        screen.blit(text, (x + 20 + 2, y - 10 + 2))


def draw_path():
    for i in range(1, len(coordinates)):
        start_x, start_y = coordinates[i - 1]
        end_x, end_y = coordinates[i]
        pygame.draw.line(screen, LINE_COLOR, (start_x*1.5, start_y*1.5), (end_x*1.5, end_y*1.5))


def draw_progress_bar(global_time):
    # Drawing the progress bar itself
    pygame.draw.rect(screen, (200, 200, 200), (PROGRESSBAR_X, PROGRESSBAR_Y, PROGRESSBAR_WIDTH, PROGRESSBAR_HEIGHT))
    pygame.draw.rect(screen, (0, 0, 0), (PROGRESSBAR_X + global_time * PROGRESSBAR_WIDTH - 2, PROGRESSBAR_Y, 4, PROGRESSBAR_HEIGHT))

    # Convert the global_time (range 0 to 1) to hours (range 0 to 24)
    # total_hours = global_time * 24
    #
    # # Extract hours and minutes
    # hours = int(total_hours)
    # minutes = int((total_hours - hours) * 60)
    #
    # # Format time as HH:mm
    # time_str = "{:02d}:{:02d}".format(hours, minutes)
    #
    # font = pygame.font.SysFont(None, 24)
    # text = font.render(time_str, True, (0, 0, 0))
    # text_width, text_height = font.size(time_str)

    # Calculate position for the text
    # text_x = PROGRESSBAR_X + global_time * PROGRESSBAR_WIDTH - text_width / 2
    # text_y = PROGRESSBAR_Y - text_height - 5  # 5 pixels gap
    #
    # # Ensure the text does not move out of screen
    # text_x = min(max(text_x, PROGRESSBAR_X), PROGRESSBAR_X + PROGRESSBAR_WIDTH - text_width)
    # screen.blit(text, (text_x, text_y))


def draw_title():
    #title_str = "Demo of battery transfer on a single railway line"  # Modify this string to your desired title
    #font = pygame.font.SysFont(None, 36)  # Adjust font size if needed
    #text = font.render(title_str, True, (0, 0, 0))
    #text_width, text_height = font.size(title_str)

    #screen.blit(text, (SCREEN_WIDTH - text_width - 50, 100))  # 10 pixels padding from the right and top edge
    #title_strs = "Melbourne CBD"  # Modify this string to your desired title
    #fonts = pygame.font.SysFont(None, 36)  # Adjust font size if needed
    #texts = font.render(title_strs, True, (0, 0, 0))
    #text_widths, text_heights = fonts.size(title_str)

    #screen.blit(texts, (SCREEN_WIDTH - text_widths +350, 850))
    pass

def main():
    global dragging
    clock = pygame.time.Clock()
    auto_move = False
    global_time = 0  # This variable keeps track of the overall time progression
    SUBURB_BATTERY_DECREMENT = 0.1
    CITY_BATTERY_DECREMENT = 0.3

    while True:
        screen.fill(BACKGROUND_COLOR)
        # Blit the image onto the screen
        screen.blit(background_image, (0, 0))

        draw_title()
        draw_path()
        if 0<=global_time<=0.45 or 0.55<=global_time<=0.75 or 0.85<=global_time<=1:
            SUBURB_BATTERY_DECREMENT = 0.1
            CITY_BATTERY_DECREMENT = 0.3
        elif 0.45<global_time<0.55:
            SUBURB_BATTERY_DECREMENT = 0.3
            CITY_BATTERY_DECREMENT = 1.2
        elif 0.75<=global_time<=0.85:
            SUBURB_BATTERY_DECREMENT = 0.3
            CITY_BATTERY_DECREMENT = 1.3

        if auto_move:
            global_time += 1/960
            if global_time > 1:
                global_time=1
                SUBURB_BATTERY_DECREMENT = 0
                CITY_BATTERY_DECREMENT = 0
            for warehouse in battery_warehouses:
                if warehouse["position"][0]<431:
                    warehouse["battery_count"] = max(-50, warehouse["battery_count"] - SUBURB_BATTERY_DECREMENT)
                else:
                    warehouse["battery_count"] = max(-50, warehouse["battery_count"] - CITY_BATTERY_DECREMENT)

        for train in trains:
            train_elapsed_time = global_time * max_time - train["start_time"]
            if 0 <= train_elapsed_time <= 1:  # If the train is within its allowed time frame
                train["percentage"] = train_elapsed_time
                update_battery_warehouses(train["percentage"], train)  # Check and refill batteries
                x, y = get_train_position(train["percentage"])
                draw_train(x, y, train["battery_count"])
        draw_battery_warehouses()
        draw_progress_bar(global_time)
        switch_color = palette.JADE if auto_move else palette.TOMATO
        pygame.draw.rect(screen, switch_color, (SWITCH_X, SWITCH_Y, SWITCH_WIDTH, SWITCH_HEIGHT))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and PROGRESSBAR_X <= event.pos[
                0] <= PROGRESSBAR_X + PROGRESSBAR_WIDTH and PROGRESSBAR_Y <= event.pos[
                1] <= PROGRESSBAR_Y + PROGRESSBAR_HEIGHT:
                dragging = True
                auto_move = False

            if event.type == pygame.MOUSEBUTTONUP:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                mouse_x = event.pos[0]
                global_time = (mouse_x - PROGRESSBAR_X) / PROGRESSBAR_WIDTH
                global_time = max(0, min(1, global_time))
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 检查是否点击了开关
                if SWITCH_X <= event.pos[0] <= SWITCH_X + SWITCH_WIDTH and SWITCH_Y <= event.pos[
                    1] <= SWITCH_Y + SWITCH_HEIGHT:
                    auto_move = not auto_move  # 切换开关状态



        clock.tick(60)





if __name__ == "__main__":
    main()