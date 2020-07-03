import os
import csv


class Mineralogy:

    def __init__(self, melts_files_path):
        self.__melts_path = melts_files_path
        self.adibekyan_bsp = {}
        self.adibekyan_morb_f1400 = {}
        self.adibekyan_morb_f1600 = {}
        self.kepler_bsp = {}
        self.kepler_morb_f1400 = {}
        self.kepler_morb_f1600 = {}

    def get_appearance_and_disappearance_temperatures(self, minerals=None):
        if minerals is None:
            minerals = ["cpx", "opx", "olivine", "fe_metal", "spinel"]

