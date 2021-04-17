import os
import csv
import pandas as pd
from scipy import integrate

class BuoyantForces:

    def __init__(self, name, bsp_path, morb_path):
        self.name = name
        self.bsp_path = bsp_path + "/fort.58"
        self.morb_path = morb_path + "/fort.58"
        self.depths = []
        self.output_file_name = name + ".csv"
        if self.output_file_name in os.listdir(os.getcwd()):
            os.remove(self.output_file_name)
        self.output_file = open(self.output_file_name, 'w')

    def specific_buoyancy(self, bsp_density, morb_density, gravity=9.8):
        density_differentials = [x - y for x, y  in zip(morb_density, bsp_density)]
        buoyancies = []
        for index, i in enumerate(density_differentials):
            if index < len(density_differentials) - 1:
                sublist_density_diffs = density_differentials[0:index + 1]
                d = self.depths[0:index + 1]
                buoyancy_force = integrate.simps(sublist_density_diffs, d) * 1000 * 1000 * gravity
                buoyancies.append(buoyancy_force)
            else:
                buoyancy_force = integrate.simps(density_differentials, self.depths) * 1000 * 1000 * gravity
                buoyancies.append(buoyancy_force)
        return buoyancies

    def calculate(self, gravity):
        first = True
        for file in os.listdir(self.bsp_path):
            if file in os.listdir(self.morb_path):
                star = file.split(".")[0]
                bsp_file_path = self.bsp_path + "/" + file
                morb_file_path = self.morb_path + "/" + file
                bsp_df = pd.read_csv(bsp_file_path)
                morb_df = pd.read_csv(morb_file_path)
                self.depths = bsp_df['depth']
                bsp_rho = bsp_df['rho']
                morb_rho = morb_df['rho']
                buoyancies = self.specific_buoyancy(bsp_density=bsp_rho, morb_density=morb_rho, gravity=gravity)
                if first:
                    header = ["star"] + list(self.depths)
                    header = ",".join(str(i) for i in header)
                    self.output_file.write(header + "\n")
                    first = False
                buoyancies = [star] + buoyancies
                buoyancies = ",".join(str(i) for i in buoyancies)
                self.output_file.write(buoyancies + "\n")
        self.output_file.close()

# (bsp_temp, morb_f_temp, morb_temp)
runs = [
    (1600, 1600, 1600),
    (1600, 1600, 1400),
    (1600, 1600, 1200),
    (1600, 1400, 1400),
    (1600, 1400, 1200),
    (1600, 1200, 1200),

    (1400, 1400, 1400),
    (1400, 1400, 1200),
    (1400, 1200, 1200),

    (1200, 1200, 1200),
]

for r in runs:
    bsp_temp, morb_f_temp, morb_temp = r

    BuoyantForces(
        name="Kepler_BSP_{}_MORB_F{}_{}".format(bsp_temp, morb_f_temp, morb_temp),
        bsp_path="/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/hefesto_output_files/Kepler_BSP/{}".format(bsp_temp),
        morb_path="/Users/scotthull/Documents - Scott’s MacBook Pro/PhD Research/hefesto_output_files/Kepler_MORB_F{}/{}".format(morb_f_temp, morb_temp)
    ).calculate(gravity=9.8)

