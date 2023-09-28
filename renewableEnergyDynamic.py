'''
Author: Yueming Wang
Date: 28 Sep 2023
'''


import sys
import pygame
from pygame.locals import *
import math
import palette as p

# 初始化Pygame
pygame.init()

# 设置窗口的大小
WIDTH, HEIGHT = 1050, 1015
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Renewable Energy Supply and Train Movement")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (200, 200, 200)
CIRCLE_COLOR = (173, 216, 230)  # Light blue color
LINE_COLOR = (0, 0, 0)

# 定义能源类型
SOLAR = "solar"
WIND = "wind"
HYDRO = "hydro"
# 定义初始天气
weather = "sunny"

# 定义初始时间
time = 48  # 12:00

# 定义字体
font = pygame.font.Font(None, 36)

# Train data: starting_time, battery_count, current_percentage
trains = [
    {"start_time": 0, "battery_count": 50, "percentage": 0},
    {"start_time": 1, "battery_count": 20, "percentage": 0},
    {"start_time": 2, "battery_count": 500, "percentage": 0},
    {"start_time": 3, "battery_count": 250, "percentage": 0},
    {"start_time": 4, "battery_count": 350, "percentage": 0},
]

coordinates = [(0, 1), (2, 5), (4, 4), (4, 6), (8, 8), (12, 9), (11, 15), (15, 20), (20, 16)]
times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]  # An example timeline
max_time = times[-1] - 1
battery_warehouses = [
    {"position": coord, "battery_count": 20} for coord in coordinates[1:]
]


# 计算supply的大小
def calculate_supply(energy_type, time, weather):
    hour = time // 4
    if energy_type == SOLAR:
        # 太阳能在白天达到最大，在夜间为0
        supply = max(0, 100 - abs(hour - 12) * 100 / 6)
        if weather == "rainy" or weather == "cloudy":
            supply *= 0.5  # 雨天或阴天时太阳能输出减半
    elif energy_type == WIND:
        # 风电根据正弦波变化
        supply = 50 + 50 * math.sin(math.radians(hour * 15))
        if weather == "rainy":
            supply *= 1.2  # 风电在雨天时增加
    elif energy_type == HYDRO:
        # 水电保持稳定输出
        supply = 90 if weather == "rainy" else 80  # 雨天时水电输出提高到90
    return supply


# 传统能源互补
def draw_gray_circle(solar_supply, wind_supply, hydro_supply):
    total_supply = solar_supply + wind_supply + hydro_supply
    remaining = int(400 - total_supply)
    pos = (WIDTH - 100, HEIGHT // 2)  # 您可以根据需要更改这个位置
    pygame.draw.circle(screen, GREY, pos, 50)  # 您可以根据需要更改半径大小
    text = font.render(str(remaining), True, WHITE)
    screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2))


# 变色逻辑
def draw_circle(energy_type, pos, time, weather):
    supply = calculate_supply(energy_type, time, weather)

    color = p.blend_colors(supply / 100, p.ZERO_CAPACITY_COLOUR, p.FULL_CAPACITY_COLOUR)

    pygame.draw.circle(screen, color, pos, 70)
    text = font.render(str(int(supply)), True, p.SCARLET)
    screen.blit(text, (pos[0] - text.get_width() // 2, pos[1] - text.get_height() // 2))


# 时间轴
def draw_time_slider(time):
    pygame.draw.rect(screen, GREY, (50, HEIGHT - 150, WIDTH - 100, 10))
    pygame.draw.circle(screen, WHITE, (50 + int(time * (WIDTH - 100) / 96), HEIGHT - 145), 15)
    hour = int(time // 4)
    minute = int((time % 4) * 15)
    time_text = font.render(f"{hour:02d}:{minute:02d}", True, WHITE)
    screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT - 175))


auto_mode = False


def draw_auto_button():
    color = GREEN if auto_mode else GREY
    pygame.draw.polygon(screen, color, [(10, HEIGHT - 195), (30, HEIGHT - 185), (10, HEIGHT - 175)])


def draw_buttons(weather):
    buttons = ["sunny", "cloudy", "rainy"]
    x = WIDTH // 2 - 120
    for button in buttons:
        color = GREEN if button == weather else GREY
        pygame.draw.rect(screen, color, (x, HEIGHT - 100, 100, 50))  # 修改按钮大小
        button_text = font.render(button, True, WHITE)
        screen.blit(button_text, (x + 10, HEIGHT - 90))
        x += 120


icon_size = (50, 50)  # 用您希望的宽度和高度替换这个值

wind_icon = pygame.image.load('src/windIcon.png').convert_alpha()
wind_icon = pygame.transform.scale(wind_icon, icon_size)

solar_icon = pygame.image.load('src/solarIcon.png').convert_alpha()
solar_icon = pygame.transform.scale(solar_icon, icon_size)

hydro_icon = pygame.image.load('src/hydroIcon.png').convert_alpha()
hydro_icon = pygame.transform.scale(hydro_icon, icon_size)


def draw_icon_and_value(icon, pos, supply):
    screen.blit(icon, (pos[0] - icon.get_width() // 2, pos[1] - icon.get_height() // 2))
    value_text = font.render(str(int(supply)), True, WHITE)
    screen.blit(value_text, (pos[0] - value_text.get_width() // 2, pos[1] + icon.get_height() // 2 + 10))


def draw_path():
    for i in range(1, len(coordinates)):
        start_x, start_y = coordinates[i - 1]
        end_x, end_y = coordinates[i]
        pygame.draw.line(screen, LINE_COLOR, (start_x * 50, start_y * 50), (end_x * 50, end_y * 50))


def get_train_position(percentage):
    time = percentage * max_time
    for i in range(len(times) - 1):
        if times[i] <= time <= times[i + 1]:
            alpha = (time - times[i]) / (times[i + 1] - times[i])
            start_x, start_y = coordinates[i]
            end_x, end_y = coordinates[i + 1]
            x_position = (1 - alpha) * start_x + alpha * end_x
            y_position = (1 - alpha) * start_y + alpha * end_y
            return x_position * 50, y_position * 50  # We scale the coordinates for better visualization
    return -1, -1  # Outside of the defined time range


def draw_train(x, y, battery_count):
    pygame.draw.circle(screen, CIRCLE_COLOR, (int(x), int(y)), battery_count / 20)
    font = pygame.font.SysFont(None, 25)
    text_surface = font.render("{:.2f}".format(battery_count), True, (0, 0, 0))
    text_rect = text_surface.get_rect(center=(int(x), int(y)))
    screen.blit(text_surface, text_rect)


def update_battery_warehouses(train_percentage, train):
    tolerance = 100
    for warehouse in battery_warehouses:
        x, y = warehouse["position"]
        train_x, train_y = get_train_position(train_percentage)
        distance = ((train_x - x * 50) ** 2 + (train_y - y * 50) ** 2) ** 0.5
        if distance < tolerance and warehouse["battery_count"] < 50:
            if train["battery_count"] >= 70 - warehouse["battery_count"]:
                train["battery_count"] = train["battery_count"] - (70 - warehouse["battery_count"])
                warehouse["battery_count"] = 70
            else:
                warehouse["battery_count"] = warehouse["battery_count"] + train["battery_count"]
                train["battery_count"] = 0


def draw_battery_warehouses():
    for warehouse in battery_warehouses:
        x, y = warehouse["position"]
        x = 50 * x
        y = 50 * y
        color = get_color_for_battery(warehouse["battery_count"])
        pygame.draw.rect(screen, color, (x - 10, y + 10, 20, 20))  # Draw a yellow square below the coordinate point
        font = pygame.font.SysFont(None, 24)
        text = font.render("{:.2f}".format(warehouse["battery_count"]), True, (0, 0, 0))
        screen.blit(text, (x - 5, y + 35))


def get_color_for_battery(battery_count):
    if battery_count <= 0:
        t = -battery_count / 50.0  # Map the range [-50, 0] to [0, 1]
        r = int(lerp(255, 0, t))
        g = int(lerp(0, 255, t))
        b = 0
    elif battery_count <= 70:
        t = battery_count / 70.0  # Map the range [0, 70] to [0, 1]
        r = 0
        g = int(lerp(255, 0, t))
        b = int(lerp(0, 255, t))
    else:
        r, g, b = 0, 0, 255  # Just blue for counts above 70
    return (r, g, b)


def lerp(a, b, t):
    """Linear interpolation between a and b."""
    return a + t * (b - a)


# 在main函数中，我们需要整合train和battery_warehouse的逻辑
def main():
    global time, weather, auto_mode
    clock = pygame.time.Clock()
    train_global_time = 0
    running = True
    dragging = False
    BATTERY_DECREMENT = 0.1

    while running:
        train_global_time = time / 196.0  # 将0到96的范围映射到0到1之间
        screen.fill(WHITE)
        # 绘制路径
        draw_path()

        # 自动增加时间

        if auto_mode:
            time = (time + 1) % 97
            for warehouse in battery_warehouses:
                warehouse["battery_count"] = max(-50, warehouse["battery_count"] - BATTERY_DECREMENT)


        # 处理火车的逻辑
        for train in trains:
            train_elapsed_time = train_global_time * max_time - train["start_time"]
            if 0 <= train_elapsed_time <= 1:  # If the train is within its allowed time frame
                train["percentage"] = train_elapsed_time
                update_battery_warehouses(train["percentage"], train)  # Check and refill batteries
                x, y = get_train_position(train["percentage"])
                draw_train(x, y, train["battery_count"])

        # 绘制电池仓库
        draw_battery_warehouses()

        # 绘制其他元素
        solar_supply = int(calculate_supply(SOLAR, time, weather))
        wind_supply = int(calculate_supply(WIND, time, weather))
        hydro_supply = int(calculate_supply(HYDRO, time, weather))
        draw_circle(SOLAR, (200, 100), time, weather)
        draw_circle(WIND, (400, 100), time, weather)
        draw_circle(HYDRO, (600, 100), time, weather)
        draw_time_slider(time)
        draw_buttons(weather)
        draw_auto_button()
        draw_gray_circle(solar_supply, wind_supply, hydro_supply)
        draw_icon_and_value(solar_icon, (200, 100), calculate_supply(SOLAR, time, weather))
        draw_icon_and_value(wind_icon, (400, 100), calculate_supply(WIND, time, weather))
        draw_icon_and_value(hydro_icon, (600, 100), calculate_supply(HYDRO, time, weather))

        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                # 检查时间滑块
                if HEIGHT - 155 < y < HEIGHT - 135 and 50 < x < WIDTH - 50:
                    dragging = True
                    time = max(0, min(96, (x - 50) * 96 / (WIDTH - 100)))
                # 检查天气按钮
                elif HEIGHT - 100 < y < HEIGHT - 60:
                    if WIDTH // 2 - 120 < x < WIDTH // 2 - 30:
                        weather = "sunny"
                    elif WIDTH // 2 < x < WIDTH // 2 + 90:
                        weather = "cloudy"
                    elif WIDTH // 2 + 120 < x < WIDTH // 2 + 210:
                        weather = "rainy"
                # 检查自动按钮
                elif HEIGHT - 200 < y < HEIGHT - 170 and 0 < x < 30:
                    auto_mode = not auto_mode  # 改变自动模式状态

            elif event.type == MOUSEBUTTONUP:
                dragging = False
            elif event.type == MOUSEMOTION and dragging:
                x, y = event.pos
                time = max(0, min(96, (x - 50) * 96 / (WIDTH - 100)))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
