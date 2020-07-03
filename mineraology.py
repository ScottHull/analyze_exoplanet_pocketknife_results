import os
import csv
import numpy as np
import copy


class Mineralogy:

    def __init__(self, melts_files_path="exoplanets/MELTS_Outputs"):
        self.__melts_path = melts_files_path
        self.minerals = []

        self.adibekyan_bsp = self.__get_appearance_and_disappearance_temperatures(dir_extension="Adibekyan_Star_Compositions_Completed_BSP_MELTS_Files")
        self.adibekyan_morb_f1400 = self.__get_appearance_and_disappearance_temperatures(dir_extension="Adibekyan_Star_Compositions_F1400_Completed_MORB_MELTS_Files")
        self.adibekyan_morb_f1600 = self.__get_appearance_and_disappearance_temperatures(dir_extension="Adibekyan_Star_Compositions_F1600_Completed_MORB_MELTS_Files")
        self.kepler_bsp = self.__get_appearance_and_disappearance_temperatures(dir_extension="Kepler_Star_Compositions_Completed_BSP_MELTS_Files")
        self.kepler_morb_f1400 = self.__get_appearance_and_disappearance_temperatures(dir_extension="Kepler_Star_Compositions_F1400_Completed_MORB_MELTS_Files")
        self.kepler_morb_f1600 = self.__get_appearance_and_disappearance_temperatures(dir_extension="Kepler_Star_Compositions_F1400_Completed_MORB_MELTS_Files")

    def __initial_tracked_setup(self, minerals):
        tracked = {}
        for i in minerals:
            tracked.update({i: {
                'appearance': np.nan,
                'disappearance': np.nan
            }})
        return tracked

    def __map_mineral_to_index(self, minerals, headers):
        mapped = {}
        for i in minerals:
            if i in headers:
                mapped.update({i: headers.index(i)})
        return mapped

    def __track_appearance_and_dissapearance(self, tracked, row, indices):
        temperature = row[1]
        mass = row[2]
        for i in tracked.keys():
            appearance = tracked[i]['appearance']
            disappearance = tracked[i]['disappearance']
            val = float(row[indices[i]])
            if np.isnan(appearance) and val != 0.0:
                tracked[i]['appearance'] = float(temperature)
            elif not np.isnan(appearance) and val == 0.0:
                tracked[i]['disappearance'] = float(temperature)


    def __get_appearance_and_disappearance_temperatures(self, dir_extension):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.__melts_path + "/{}".format(dir_extension)):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        stars = {}
        for index, i in enumerate(fnames):
            star = i.replace("__BSP_OUTPUT.csv", "").replace("_M_MORB_OUTPUT.csv", "")
            if not str(star).endswith(".csv") or not str(star).endswith(".py"):
                f = files[index]
                with open(f, 'r') as infile:
                    reader = csv.reader(infile, delimiter=",")
                    FOUND = False
                    headers = []
                    tracked = {}
                    mineral_indices = {}
                    for row in reader:
                        if not len(row) == 0:
                            if row[0] == "Phase" and row[1] == "Masses:":
                                FOUND = True
                                headers = list(next(reader))
                                if "" in headers:
                                    headers.remove("")
                                minerals = copy.copy(headers)
                                minerals.remove("liquid_0")
                                minerals.remove("Pressure")
                                minerals.remove("Temperature")
                                minerals.remove("mass")
                                if "" in minerals:
                                    minerals.remove("")
                                for j in minerals:
                                    if j not in self.minerals:
                                        self.minerals.append(j)
                                tracked = self.__initial_tracked_setup(minerals=minerals)
                                mineral_indices = self.__map_mineral_to_index(minerals=minerals, headers=headers)
                            elif FOUND is True:
                                self.__track_appearance_and_dissapearance(tracked=tracked, row=row, indices=mineral_indices)
                        else:
                            if FOUND:
                                stars.update({star: tracked})
                                break
                infile.close()
        return stars

    def get_appearance_and_disappearance_temperatures(self):
        return {
            "adibekyan_bsp": self.adibekyan_bsp,
            "adibekyan_morb_f1400": self.adibekyan_morb_f1400,
            "adibekyan_morb_f1600": self.adibekyan_morb_f1600,
            "kepler_bsp": self.kepler_bsp,
            "kepler_morb_f1400": self.kepler_morb_f1400,
            "kepler_morb_f1600": self.kepler_morb_f1600
        }

    def get_all_unique_minerals_found(self):
        return self.minerals
