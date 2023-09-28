WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
TOMATO = (254, 94, 65)
JADE = (0, 168, 120)
MINDARO = (216, 241, 160)
EARTH_YELLOW = (243, 193, 120)
AQUAMARINE = (0, 224, 161)
SCARLET = (254, 48, 11)

# Pick colours
FULL_CAPACITY_COLOUR = JADE
ZERO_CAPACITY_COLOUR = TOMATO
SLIDER_COLOUR = MINDARO
KNOB_COLOUR = EARTH_YELLOW
FULL_TRAIN = AQUAMARINE
EMPTY_TRAIN = SCARLET


# Colour change function for capacity display
def colour(capacity=0):
    scale_factor = (capacity + 100) / 200

    return blend_colors(scale_factor, ZERO_CAPACITY_COLOUR, FULL_CAPACITY_COLOUR)


def blend_colors(factor, color1, color2):
    """
    Blend two colors using a factor.

    Parameters:
    - factor (float): A value between 0 and 1, where 0 represents color1 and 1 represents color2.
    - color1 (tuple): A tuple representing the first color (R, G, B).
    - color2 (tuple): A tuple representing the second color (R, G, B).

    Returns:
    - tuple: A blended color (R, G, B).
    """

    if 0 > factor:
        return color1
    elif factor > 1:
        return color2

    R = round(color1[0] + (color2[0] - color1[0]) * factor)
    G = round(color1[1] + (color2[1] - color1[1]) * factor)
    B = round(color1[2] + (color2[2] - color1[2]) * factor)

    return R, G, B

