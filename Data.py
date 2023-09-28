from polygon import *
from demandCurve import consumption
from random import randrange
from palette import *

TIME_INTERVAL = 0.25  # Sample every 15 mins

# # The capacity array records for every polygon
# capacity_list = [[INIT_CAPACITY for i in range(int(24 / TIME_INTERVAL) + 1)] for j in range(len(polygons))]
# INIT_CAPACITY = 100  # %
#
# polygon_idx = 0
# for capacity in capacity_list:
#     # iterate through each time-capacity array
#     for i in range(1, len(capacity)):
#         # Iterate through each time, time given by i*0.25
#         t = i * 0.25
#
#         # Get the demand variation factor from the data
#         if polygon_idx in highestDemand_polygons:
#             demand_factor = HIGHEST_DEMAND_WEIGHT
#         elif polygon_idx in middleDemand_polygons:
#             demand_factor = MIDDLE_DEMAND_WEIGHT
#         else:
#             demand_factor = LOWEST_DEMAND_WEIGHT
#
#         # The factor is a temp value
#         capacity[i] = capacity[i-1] - 0.04 * consumption(t, demand_factor=demand_factor, deviation=1)
#
#     # Increment counter
#     polygon_idx += 1


def get_capacity(demand_factor):
    # demand_factor < 2
    # A random deviation -10% ~ 10%
    # target capacity = (deviation * demand factor + 1) * average_capacity
    deviation = randrange(-DEVIATION, DEVIATION) / 100
    print((deviation * demand_factor + 1) * AVERAGE_CAPACITY)
    return (deviation * demand_factor + 1) * AVERAGE_CAPACITY


AVERAGE_CAPACITY: int = 80
DEVIATION: int = round((100 - AVERAGE_CAPACITY) / 2)

capacity_list = []

# Initialise capacity_list
for polygon_idx in range(len(polygons)):
    if polygon_idx in highestDemand_polygons:
        demand_factor = HIGHEST_DEMAND_WEIGHT
    elif polygon_idx in middleDemand_polygons:
        demand_factor = MIDDLE_DEMAND_WEIGHT
    else:
        demand_factor = LOWEST_DEMAND_WEIGHT

    capacity_list.append(get_capacity(demand_factor))


# Update capacity_list
def update_capacity_list(caps):
    for idx in range(len(caps)):
        if idx in highestDemand_polygons:
            df = HIGHEST_DEMAND_WEIGHT
        elif idx in middleDemand_polygons:
            df = MIDDLE_DEMAND_WEIGHT
        else:
            df = LOWEST_DEMAND_WEIGHT

        old_capacity = caps[idx]
        new_capacity = old_capacity + randrange(-DEVIATION, DEVIATION) * df
        new_capacity %= 100
        caps[idx] = new_capacity

    return caps



