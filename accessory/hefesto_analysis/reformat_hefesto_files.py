import csv
import os
import shutil
import pandas as pd


class HeFESToReformat:

    def __init__(self, from_path, to_path):
        self.from_path = from_path
        self.to_path = to_path
        self.base_path_name = None
        self.temperature_paths = []
        self.fort_paths = []

    def __mkdir(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)

    def __walk(self):
        self.temperature_paths = [self.from_path + "/" + i for i in os.listdir(self.from_path) if i[0] != "."]
        for temp_path in self.temperature_paths:
            current_temp = temp_path.split("/")[-1]
            to_temp_path = self.to_path + "/" + current_temp
            self.__mkdir(to_temp_path)
            self.fort_paths = [temp_path + "/" + i for i in os.listdir(temp_path) if i[0] != "."]
            for fort_path in self.fort_paths:
                current_fort = fort_path.split("/")[-1]
                to_fort_path = to_temp_path + "/" + current_fort
                self.__mkdir(to_fort_path)
                for file in os.listdir(fort_path):
                    file_path = fort_path + "/" + file
                    star = file.split("_")[0]
                    print(star)
                    try:
                        df = pd.read_fwf(file_path, header=None)
                        df.to_csv(to_fort_path + "/" + star + ".csv", index=None, header=None)
                    except:
                        pass

    def reformat(self):
        self.__walk()


# HeFESToReformat(
#     from_path="C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/raw/morb/adibekyan_morb_f1600_HeFESTo_Output_Files",
#     to_path="C:/Users/Scott/Desktop/3_26_2021/adibekyan/hefesto_output_files/csv/morb/f1600"
# ).reformat()

HeFESToReformat(
    from_path="C:/Users/Scott/Desktop/kep_depleted_lithosphere/kep_dl_f1400_HeFESTo_Output_Files",
    to_path="C:/Users/Scott/Desktop/kep_dl_csv/f1400"
).reformat()
