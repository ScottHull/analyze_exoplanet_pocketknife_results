import csv

import pandas as pd
import matplotlib.pyplot as plt

fpath = "C:/Users/Scott/Desktop/3_26_2021/summary/specific_buoyancy/"

template = "Kepler_BSP_{}_MORB_F{}_{}.csv"

# BSP temperature, MORB F temperature, MORB temperature
runs = [
    (1600, 1600, 1600),
    (1600, 1600, 1400),
    (1600, 1400, 1400),
    (1400, 1400, 1400),
]

depths = []
fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
for r in runs:
    bsp_temp, morb_f_temp, morb_temp = r[0], r[1], r[2]
    f = fpath + template.format(bsp_temp, morb_f_temp, morb_temp)
    with open(f, 'r') as infile:
        reader = csv.reader(infile)
        depths = next(reader)[1:]
        for row in reader:
            if row[0] == 'Sun':
                print(depths)
                ax.plot(
                    [float(i) for i in depths],
                    [float(i) for i in row[1:]],
                    linewidth=2.0,
                    label="BSP {}, MORB F{} @ {}".format(bsp_temp, morb_f_temp, morb_temp)
                )
                break
ax.set_xlabel('Depth (km)')
ax.set_ylabel("Specific Buoyancy")
ax.set_title("Sun")
ax.grid()
ax.legend()
plt.show()

