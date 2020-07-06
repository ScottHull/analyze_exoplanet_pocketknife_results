import os
import csv
from scipy import integrate
from src.thickness import Thickness

DEPTHS = [-1.0 * i for i in [0, 6, 19.7, 28.9, 36.4, 43.88, 51.34, 58.81, 66.36, 73.94, 81.5, 88.97, 96.45, 103.93, 111.41,
          118.92, 126.47, 134.01, 141.55, 149.09, 156.64, 164.18, 171.72, 179.27, 186.79, 194.27, 201.75,
          209.23, 216.71, 224.09, 231.4, 238.7, 246.01, 253.31, 260.62, 267.9, 275.16, 282.42, 289.68,
          296.94, 304.19, 311.41, 318.44, 325.47, 332.5, 339.53, 346.56, 353.59, 360.62, 367.66, 374.69,
          381.72, 388.75, 395.78, 402.78, 409.72, 416.67, 423.61, 430.56, 437.5, 444.44, 451.32, 457.89,
          464.47, 471.05, 477.63, 484.21, 490.79, 497.37, 503.75, 510, 516.25, 522.5, 528.75, 535, 541.25,
          547.5, 553.95, 560.53, 567.11, 573.68]]


class Inspect:

    def __init__(self, reg_path="src/exoplanets/Densities/BSP_MORB",
                 depleted_path="src/exoplanets/Densities/Depleted_Lithosphere", get_actual_mass_fractions=True,
                 initial_morb_mass_path="src/exoplanets/starting_morb_masses",
                 final_morb_mass_path="src/exoplanets/final_morb_masses"):
        super().__init__()
        self.reg_path = reg_path
        self.depleted_path = depleted_path
        self.__get_actual_mass_fractions = get_actual_mass_fractions
        self.adibekyan_bsp_1200 = None
        self.adibekyan_bsp_1400 = None
        self.adibekyan_bsp_1600 = None
        self.adibekyan_depleted_bsp_f1200_1200 = None
        self.adibekyan_depleted_bsp_f1400_1200 = None
        self.adibekyan_depleted_bsp_f1400_1400 = None
        self.adibekyan_depleted_bsp_f1600_1200 = None
        self.adibekyan_depleted_bsp_f1600_1400 = None
        self.adibekyan_depleted_bsp_f1600_1600 = None
        self.adibekyan_morb_f1200_1200 = None
        self.adibekyan_morb_f1400_1200 = None
        self.adibekyan_morb_f1400_1400 = None
        self.adibekyan_morb_f1600_1200 = None
        self.adibekyan_morb_f1600_1400 = None
        self.adibekyan_morb_f1600_1600 = None
        self.kepler_bsp_1200 = None
        self.kepler_bsp_1400 = None
        self.kepler_bsp_1600 = None
        self.kepler_depleted_bsp_f1200_1200 = None
        self.kepler_depleted_bsp_f1400_1200 = None
        self.kepler_depleted_bsp_f1400_1400 = None
        self.kepler_depleted_bsp_f1600_1200 = None
        self.kepler_depleted_bsp_f1600_1400 = None
        self.kepler_depleted_bsp_f1600_1600 = None
        self.kepler_morb_f1200_1200 = None
        self.kepler_morb_f1400_1200 = None
        self.kepler_morb_f1400_1400 = None
        self.kepler_morb_f1600_1200 = None
        self.kepler_morb_f1600_1400 = None
        self.kepler_morb_f1600_1600 = None

        self.__getfiles()

        if self.__get_actual_mass_fractions:
            self.thicknesses = Thickness(initial_mass_path=initial_morb_mass_path, final_mass_path=final_morb_mass_path)

    def __return_df(self, f):
        return list(csv.reader(open(f, 'r'), delimiter=","))

    def __getfiles(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.reg_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "Adibekyan" in i and "BSP" in i and "1200" in i:
                self.adibekyan_bsp_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "BSP" in i and "1400" in i:
                self.adibekyan_bsp_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "BSP" in i and "1600" in i:
                self.adibekyan_bsp_1600 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1200" in i and "_1200" in i:
                self.adibekyan_morb_f1200_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1400" in i and "_1200" in i:
                self.adibekyan_morb_f1400_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1400" in i and "_1400" in i:
                self.adibekyan_morb_f1400_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1200" in i:
                self.adibekyan_morb_f1600_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1400" in i:
                self.adibekyan_morb_f1600_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "MORB" in i and "_F1600" in i and "_1600" in i:
                self.adibekyan_morb_f1600_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1200" in i:
                self.kepler_bsp_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1400" in i:
                self.kepler_bsp_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "BSP" in i and "1600" in i:
                self.kepler_bsp_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1200" in i and "_1200" in i:
                self.kepler_morb_f1200_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1400" in i and "_1200" in i:
                self.kepler_morb_f1400_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1400" in i and "_1400" in i:
                self.kepler_morb_f1400_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1200" in i:
                self.kepler_morb_f1600_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1400" in i:
                self.kepler_morb_f1600_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "MORB" in i and "_F1600" in i and "_1600" in i:
                self.kepler_morb_f1600_1600 = self.__return_df(f=f)

        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.depleted_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "Adibekyan" in i and "F1200" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1200_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1400" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1400_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1400" in i and "_1400" in i:
                self.adibekyan_depleted_bsp_f1400_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1200" in i:
                self.adibekyan_depleted_bsp_f1600_1200 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1400" in i:
                self.adibekyan_depleted_bsp_f1600_1400 = self.__return_df(f=f)
            elif "Adibekyan" in i and "F1600" in i and "_1600" in i:
                self.adibekyan_depleted_bsp_f1600_1600 = self.__return_df(f=f)
            elif "Kepler" in i and "F1200" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1200_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1400" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1400_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1400" in i and "_1400" in i:
                self.kepler_depleted_bsp_f1400_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1200" in i:
                self.kepler_depleted_bsp_f1600_1200 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1400" in i:
                self.kepler_depleted_bsp_f1600_1400 = self.__return_df(f=f)
            elif "Kepler" in i and "F1600" in i and "_1600" in i:
                self.kepler_depleted_bsp_f1600_1600 = self.__return_df(f=f)

    def __get_morb_row(self, star, morb_file):
        for row in morb_file:
            if row[0] == star:
                return row
        return []

    def __get_earth_row(self, file):
        for row in file:
            if row[0].lower() == "sun":
                return row

    def __calc_buoyancy_with_depth(self, density_differentials, d, plate_thickness=10 * 1000, gravity=9.8):
        return integrate.simps(density_differentials, d) * 1000 * 1000 * plate_thickness * gravity

    def __compute_buoyancy_at_depth(self, density_differentials, f=10.0):
        buoyancies = []
        for index, i in enumerate(density_differentials):
            if index < len(density_differentials) - 1:
                sublist_density_diffs = density_differentials[0:index + 1]
                d = DEPTHS[0:index + 1]
                buoyancy_force = self.__calc_buoyancy_with_depth(density_differentials=sublist_density_diffs, d=d)
                buoyancies.append(buoyancy_force)
            else:
                buoyancy_force = self.__calc_buoyancy_with_depth(density_differentials=density_differentials, d=DEPTHS)
                buoyancies.append(buoyancy_force)
        return buoyancies

    def __get_mass_fraction(self, morb_name):
        if "adibekyan" in morb_name and "f1400" in morb_name:
            return self.thicknesses.adibekyan_f1400_mass_fraction
        elif "adibekyan" in morb_name and "f1600" in morb_name:
            return self.thicknesses.adibekyan_f1600_mass_fraction
        elif "kepler" in morb_name and "f1400" in morb_name:
            return self.thicknesses.kepler_f1400_mass_fraction
        elif "kepler" in morb_name and "f1600" in morb_name:
            return self.thicknesses.kepler_f1600_mass_fraction

    def get_buoyancy(self, bsp_file, morb_file, morb_name=None):
        buoyancies = {}

        if self.__get_actual_mass_fractions and morb_name is not None:
            f = self.__get_mass_fraction(morb_name=morb_name)

        for bsp_row in bsp_file:
            star = bsp_row[0]
            morb_row = self.__get_morb_row(star=star, morb_file=morb_file)
            if len(bsp_row[1:]) == len(morb_row[1:]) == len(DEPTHS):
                density_differences = [float(x) - float(y) for x, y in zip(morb_row[1:], bsp_row[1:])]
                if self.__get_actual_mass_fractions and morb_name is not None:
                    if star in f.keys():
                        buoyancy_force = self.__compute_buoyancy_at_depth(density_differentials=density_differences,
                                                                      f=f[star])
                    else:
                        buoyancy_force = self.__compute_buoyancy_at_depth(density_differentials=density_differences)
                else:
                    buoyancy_force = self.__compute_buoyancy_at_depth(density_differentials=density_differences)
                buoyancies.update({star: buoyancy_force})

        return buoyancies
