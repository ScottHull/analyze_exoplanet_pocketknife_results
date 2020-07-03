import os
import numpy as np
import pandas as pd


class Thickness:

    def __init__(self, initial_mass_path, final_mass_path):
        self.__initial_masses_path = initial_mass_path
        self.__final_masses_path = final_mass_path

        self.adibekyan_f1400_initial_morb_mass = {}
        self.adibekyan_f1600_initial_morb_mass = {}
        self.kepler_f1400_initial_morb_mass = {}
        self.kepler_f1600_initial_morb_mass = {}

        self.adibekyan_f1400_final_morb_mass = {}
        self.adibekyan_f1600_final_morb_mass = {}
        self.kepler_f1400_final_morb_mass = {}
        self.kepler_f1600_final_morb_mass = {}

        self.__get_initial_MORB_melt_masses()
        self.__get_final_MORB_melt_masses()

        self.adibekyan_f1400_mass_fraction = self.__calc_mass_fraction(
            initial_dict=self.adibekyan_f1400_initial_morb_mass, final_dict=self.adibekyan_f1400_final_morb_mass)
        self.adibekyan_f1600_mass_fraction = self.__calc_mass_fraction(
            initial_dict=self.adibekyan_f1600_initial_morb_mass, final_dict=self.adibekyan_f1600_final_morb_mass)
        self.kepler_f1400_mass_fraction = self.__calc_mass_fraction(
            initial_dict=self.kepler_f1400_initial_morb_mass, final_dict=self.kepler_f1400_final_morb_mass)
        self.kepler_f1600_mass_fraction = self.__calc_mass_fraction(
            initial_dict=self.kepler_f1600_initial_morb_mass, final_dict=self.kepler_f1600_final_morb_mass)

    def __initial_mass_dict(self, df):
        d = {}
        for row in df.index:
            star = df['star'][row]
            m = df['initial_mass'][row]
            d.update({star: m})
        return d

    def __final_mass_dict(self, df):
        d = {}
        for row in df.index:
            star = df['Star'][row]
            m = df['Mass'][row]
            d.update({star: m})
        return d

    def __get_initial_MORB_melt_masses(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.__initial_masses_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "adibekyan" in f and "f1400" in f:
                self.adibekyan_f1400_initial_morb_mass = self.__initial_mass_dict(pd.read_csv(f, delimiter=","))
            elif "adibekyan" in f and "f1600" in f:
                self.adibekyan_f1600_initial_morb_mass = self.__initial_mass_dict(pd.read_csv(f, delimiter=","))
            elif "kepler" in f and "f1400" in f:
                self.kepler_f1400_initial_morb_mass = self.__initial_mass_dict(pd.read_csv(f, delimiter=","))
            elif "kepler" in f and "f1600" in f:
                self.kepler_f1600_initial_morb_mass = self.__initial_mass_dict(pd.read_csv(f, delimiter=","))

    def __get_final_MORB_melt_masses(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.__final_masses_path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "adibekyan" in f and "f1400" in f:
                self.adibekyan_f1400_final_morb_mass = self.__final_mass_dict(pd.read_csv(f, delimiter=","))
            elif "adibekyan" in f and "f1600" in f:
                self.adibekyan_f1600_final_morb_mass = self.__final_mass_dict(pd.read_csv(f, delimiter=","))
            elif "kepler" in f and "f1400" in f:
                self.kepler_f1400_final_morb_mass = self.__final_mass_dict(pd.read_csv(f, delimiter=","))
            elif "kepler" in f and "f1600" in f:
                self.kepler_f1600_final_morb_mass = self.__final_mass_dict(pd.read_csv(f, delimiter=","))

    def __calc_mass_fraction(self, initial_dict, final_dict):
        mass_fractions = {}
        for s in initial_dict.keys():
            if s in final_dict.keys():
                final = final_dict[s]
                if not np.isnan(initial_dict[s]) and not np.isnan(final_dict[s]):
                    initial = initial_dict[s]
                    mass_fractions.update({s: (final / initial) * 100.0})
        return mass_fractions
