import os
import csv
import pandas as pd
from scipy import integrate

"""
    This code requires that the HeFESTo inputs be reformatted to CSV.
"""


class BuoyantForces:

    def __init__(self, name, path):
        self.name = name
        self.path = path + "/fort.58"
        self.depths = []
        self.output_file_name = name + ".csv"
        if self.output_file_name in os.listdir(os.getcwd()):
            os.remove(self.output_file_name)
        self.output_file = open(self.output_file_name, 'w')

    def calculate(self):
        first = True
        for file in os.listdir(self.path):
            star = None
            try:
                star = file.split(".")[0]
                bsp_file_path = self.path + "/" + file
                df = pd.read_csv(bsp_file_path)
                self.depths = df['depth']
                if first:
                    self.output_file.write("star" + "," + ",".join(str(i) for i in self.depths) + "\n")
                    first = False
                rho = df['rho']
                rhos = star + "," + ",".join(str(i) for i in rho)
                self.output_file.write(rhos + "\n")
            except:
                print("Problem with {}".format(star))
                pass
        self.output_file.close()


# (bsp_temp, morb_f_temp, morb_temp)
# runs = [
#     (1600, 1600, 1600),
#     (1600, 1600, 1400),
#     (1600, 1600, 1200),
#     (1600, 1400, 1400),
#     (1600, 1400, 1200),
#     # (1600, 1200, 1200),
#
#     (1400, 1400, 1400),
#     (1400, 1400, 1200),
#     # (1400, 1200, 1200),
#
#     # (1200, 1200, 1200),
# ]

# runs = [1600, 1400, 1200]
#
# for r in runs:
#
#     BuoyantForces(
#         name="Kepler_Density_BSP_{}".format(r),
#         path="C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/bsp/{}".format(r)
#     ).calculate()

# runs = [
#     (1600, 1600),
#     (1600, 1400),
#     (1600, 1200),
#
#     (1400, 1400),
#     (1400, 1200)
# ]
#
# for r in runs:
#     ftemp, temp = r[0], r[1]
#
#     BuoyantForces(
#         name="Kepler_Density_MORB_F{}_{}".format(ftemp, temp),
#         path="C:/Users/Scott/Desktop/3_26_2021/kepler/hefesto_output_files/csv/morb/f{}/{}".format(ftemp, temp)
#     ).calculate()

runs = [
    (1600, 1600),
    (1600, 1400),
    (1600, 1200),

    (1400, 1400),
    (1400, 1200)
]

for r in runs:
    ftemp, temp = r[0], r[1]

    BuoyantForces(
        name="Kepler_DEPLETED_LITHOSPHERE_Density_F{}_{}".format(ftemp, temp),
        path="C:/Users/Scott/Desktop/3_26_2021/kep_dl_csv/f{}/{}".format(ftemp, temp)
    ).calculate()
