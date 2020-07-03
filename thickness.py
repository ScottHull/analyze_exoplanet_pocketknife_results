import os
import pandas as pd



class Thickness:

    def __init__(self, initial_mass_path, final_mass_path):
        self.__initial_masses_path = initial_mass_path
        self.__final_masses_path = final_mass_path
        self.adibekyan_f1400_initial_morb_mass = None
        self.adibekyan_f1600_initial_morb_mass = None
        self.kepler_f1400_initial_morb_mass = None
        self.kepler_f1600_initial_morb_mass = None

    def __initial_mass_dict(self, df):
        d = {}
        for row in df.index:
            star = df[0][row]
            m = df[1][row]
            d.update({star: m})
        return d

    def get_initial_MORB_melt_masses(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.__initial_masses_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "Adibekyan" in f and "f1400" in f:
                df = pd.read_csv(f, header=None, delimiter=",")
