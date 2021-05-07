import csv
import matplotlib.pyplot as plt

runs = [
    (1600, 1600, 1600),
    (1600, 1600, 1400),
    # (1600, 1600, 1200),
    (1600, 1400, 1400),
    # (1600, 1400, 1200),
    # (1600, 1200, 1200),

    (1400, 1400, 1400),
    # (1400, 1400, 1200),
    # (1400, 1200, 1200),

    # (1200, 1200, 1200),
]

for r in runs:
    bsp_temp, morb_ftemp, initial_temp = r[0], r[1], r[2]

    kepler_path = "C:/Users/Scott/Desktop/3_26_2021/kepler/specific_buoyancy/Kepler_BSP_{}_MORB_F{}_{}.csv".format(bsp_temp, morb_ftemp, initial_temp)
    adibekyan_path = "C:/Users/Scott/Desktop/3_26_2021/adibekyan/specific_buoyancy/Adibekyan_BSP_{}_MORB_F{}_{}.csv".format(bsp_temp, morb_ftemp, initial_temp)

    buoyancy_pass = []
    buoyancy_fail = []

    kepler_set = list(csv.reader(open(kepler_path, 'r')))
    adibekyan_set = list(csv.reader(open(adibekyan_path, 'r')))
    earth_buoyancies = []

    depths = kepler_set[0][1:]
    kepler_set = kepler_set[1:]
    adibekyan_set = adibekyan_set[1:]

    for row in kepler_set:
        star = row[0]
        buoyancies = row[1:]
        if len(buoyancies) == len(depths):
            if star == "Sun":
                earth_buoyancies = buoyancies
                break

    for row in kepler_set:
        star = row[0]
        buoyancies = row[1:]
        if len(buoyancies) == len(depths):
            if buoyancies[-1] <= earth_buoyancies[-1]:
                buoyancy_pass.append(buoyancies)
            else:
                buoyancy_fail.append(buoyancies)

    for row in adibekyan_set:
        star = row[0]
        buoyancies = row[1:]
        if len(buoyancies) == len(depths):
            if buoyancies[-1] <= earth_buoyancies[-1]:
                buoyancy_pass.append(buoyancies)
            else:
                buoyancy_fail.append(buoyancies)
