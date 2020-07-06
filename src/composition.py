import os
import csv
import pandas as pd


class Compositions:

    def __init__(self):
        self.adibekyan_bsp = None
        self.adibekyan_morb_f1400 = None
        self.adibekyan_morb_f1600 = None
        self.adibekyan_depleted_bsp_f1400 = None
        self.adibekyan_depleted_bsp_f1600 = None
        self.kepler_bsp = None
        self.kepler_morb_f1400 = None
        self.kepler_morb_f1600 = None
        self.kepler_depleted_bsp_f1400 = None
        self.kepler_depleted_bsp_f1600 = None


class Inspect(Compositions):

    def __init__(self, path="src/exoplanets/Depleted_Lithosphere_Compositions"):
        super().__init__()
        self.path = path
        self.__melts_path = "src/exoplanets/MELTS_Outputs"

        self.__read_files()

    def __return_df(self, f):
        return pd.read_csv(f)

    def __read_files(self):
        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(self.path):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if "adibekyan" in i and "bsp" in i and "depleted_lithosphere" not in i:
                self.adibekyan_bsp = self.__return_df(f=f)
            elif "adibekyan" in i and "morb" in i and "f1400" in i and "depleted_lithosphere" not in i:
                self.adibekyan_morb_f1400 = self.__return_df(f=f)
            elif "adibekyan" in i and "morb" in i and "f1600" in i and "depleted_lithosphere" not in i:
                self.adibekyan_morb_f1600 = self.__return_df(f=f)
            elif "adibekyan" in i and "f1400" in i and "depleted_lithosphere" in i:
                self.adibekyan_depleted_bsp_f1400 = self.__return_df(f=f)
            elif "adibekyan" in i and "f1600" in i and "depleted_lithosphere" in i:
                self.adibekyan_depleted_bsp_f1600 = self.__return_df(f=f)
            elif "kepler" in i and "bsp" in i and "depleted_lithosphere" not in i:
                self.kepler_bsp = self.__return_df(f=f)
            elif "kepler" in i and "morb" in i and "f1400" in i and "depleted_lithosphere" not in i:
                self.kepler_morb_f1400 = self.__return_df(f=f)
            elif "kepler" in i and "morb" in i and "f1600" in i and "depleted_lithosphere" not in i:
                self.kepler_morb_f1600 = self.__return_df(f=f)
            elif "kepler" in i and "f1400" in i and "depleted_lithosphere" in i:
                self.kepler_depleted_bsp_f1400 = self.__return_df(f=f)
            elif "kepler" in i and "f1600" in i and "depleted_lithosphere" in i:
                self.kepler_depleted_bsp_f1600 = self.__return_df(f=f)

    def __get_depleted_row(self, star, depleted_df):
        for row in depleted_df.index:
            if star == depleted_df['Star'][row]:
                return row
        return None

    def __quant_depletion(self, daughter_reservoir_oxide, parent_reservoir_oxide):
        return ((daughter_reservoir_oxide - parent_reservoir_oxide) / parent_reservoir_oxide) * 100.0

    def get_depletion(self, parent_reservoir, daughter_reservoir):
        depletion_percentages = {}

        for row in parent_reservoir.index:
            star = parent_reservoir['Star'][row]
            parent_reservoir_feo = parent_reservoir['FeO'][row]
            parent_reservoir_na2o = parent_reservoir['Na2O'][row]
            parent_reservoir_mgo = parent_reservoir['MgO'][row]
            parent_reservoir_al2o3 = parent_reservoir['Al2O3'][row]
            parent_reservoir_sio2 = parent_reservoir['SiO2'][row]
            parent_reservoir_cao = parent_reservoir['CaO'][row]
            parent_reservoir_tio2 = parent_reservoir['TiO2'][row]

            depleted_row = self.__get_depleted_row(star=star, depleted_df=daughter_reservoir)
            if depleted_row is not None:
                daughter_reservoir_feo = daughter_reservoir['FeO'][row]
                daughter_reservoir_na2o = daughter_reservoir['Na2O'][row]
                daughter_reservoir_mgo = daughter_reservoir['MgO'][row]
                daughter_reservoir_al2o3 = daughter_reservoir['Al2O3'][row]
                daughter_reservoir_sio2 = daughter_reservoir['SiO2'][row]
                daughter_reservoir_cao = daughter_reservoir['CaO'][row]
                daughter_reservoir_tio2 = daughter_reservoir['TiO2'][row]

                depletion_feo = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_feo,
                                                       daughter_reservoir_oxide=daughter_reservoir_feo)
                depletion_na2o = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_na2o,
                                                        daughter_reservoir_oxide=daughter_reservoir_na2o)
                depletion_mgo = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_mgo,
                                                       daughter_reservoir_oxide=daughter_reservoir_mgo)
                depletion_al2o3 = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_al2o3,
                                                         daughter_reservoir_oxide=daughter_reservoir_al2o3)
                depletion_sio2 = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_sio2,
                                                        daughter_reservoir_oxide=daughter_reservoir_sio2)
                depletion_cao = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_cao,
                                                       daughter_reservoir_oxide=daughter_reservoir_cao)
                depletion_tio2 = self.__quant_depletion(parent_reservoir_oxide=parent_reservoir_tio2,
                                                        daughter_reservoir_oxide=daughter_reservoir_tio2)

                depletion_pct = {
                    'feo': depletion_feo,
                    'na2o': depletion_na2o,
                    'mgo': depletion_mgo,
                    'al2o3': depletion_al2o3,
                    'sio2': depletion_sio2,
                    'cao': depletion_cao,
                    'tio2': depletion_tio2
                }

                depletion_percentages.update({star: depletion_pct})

        return depletion_percentages

    def get_composition(self, df):
        d = {}
        for row in df.index:
            star = df['Star'][row]
            feo = df['FeO'][row]
            na2o = df['Na2O'][row]
            mgo = df['MgO'][row]
            al2o3 = df['Al2O3'][row]
            sio2 = df['SiO2'][row]
            cao = df['CaO'][row]
            tio2 = df['TiO2'][row]

            d.update({star: {
                'feo': feo,
                'na2o': na2o,
                'mgo': mgo,
                'al2o3': al2o3,
                'sio2': sio2,
                'cao': cao,
                'tio2': tio2
            }})

        return d

    def __get_dir_extension(self, keywords):
        if "adibekyan" in keywords and "bsp" in keywords:
            return "Adibekyan_Star_Compositions_Completed_BSP_MELTS_Files"
        elif "adibekyan" in keywords and "f1400" in keywords:
            return "Adibekyan_Star_Compositions_F1400_Completed_MORB_MELTS_Files"
        elif "adibekyan" in keywords and "f1600" in keywords:
            return "Adibekyan_Star_Compositions_F1600_Completed_MORB_MELTS_Files"
        elif "kepler" in keywords and "bsp" in keywords:
            return "Kepler_Star_Compositions_Completed_BSP_MELTS_Files"
        elif "kepler" in keywords and "f1400" in keywords:
            return "Kepler_Star_Compositions_F1400_Completed_MORB_MELTS_Files"
        elif "kepler" in keywords and "f1600" in keywords:
            return "Kepler_Star_Compositions_F1600_Completed_MORB_MELTS_Files"

    def __map_oxide_to_indices(self, header_row, oxides):
        d = {}
        for i in oxides:
            d.update({i.lower(): header_row.index(i)})
        return d

    def get_liquid_compositional_profile_of_star(self, star, name_keywords=None):
        if name_keywords is None:
            name_keywords = ["Adibekyan", "BSP"]
        name_keywords = [i.lower() for i in name_keywords]
        d = {
            "feo": [],
            "na2o": [],
            "mgo": [],
            "al2o3": [],
            "sio2": [],
            "cao": [],
            "tio2": [],
            "temperature": []
        }

        all_oxides = ["FeO", "Na2O", "MgO", "Al2O3", "SiO2", "CaO", "TiO2", "Temperature"]

        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(
                self.__melts_path + "/{}".format(self.__get_dir_extension(keywords=name_keywords))):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if str(star) in str(f):
                FOUND = False
                with open(f, 'r') as infile:
                    reader = csv.reader(infile, delimiter=",")
                    mapped_indices = {}
                    for row in reader:
                        if len(row) > 0:
                            if "liquid_0" in row[0]:
                                header = list(next(reader))
                                mapped_indices = self.__map_oxide_to_indices(header_row=header,
                                                                             oxides=all_oxides)
                                FOUND = True
                            elif FOUND:
                                for j in mapped_indices.keys():
                                    d[j].append(float(row[mapped_indices[j]]))
                        elif FOUND is True:
                            if len(row) == 0:
                                infile.close()
                                break
        return d

    def get_liquid_compositional_mass_fraction_profile_of_star(self, star, name_keywords=None):
        if name_keywords is None:
            name_keywords = ["Adibekyan", "BSP"]
        name_keywords = [i.lower() for i in name_keywords]
        d = {
            "feo": [],
            "na2o": [],
            "mgo": [],
            "al2o3": [],
            "sio2": [],
            "cao": [],
            "tio2": [],
            "temperature": [],
            "mass": []
        }

        all_oxides = ["FeO", "Na2O", "MgO", "Al2O3", "SiO2", "CaO", "TiO2", "Temperature", "mass"]

        files = []
        fnames = []
        for dirname, dirnames, f in os.walk(
                self.__melts_path + "/{}".format(self.__get_dir_extension(keywords=name_keywords))):
            for i in f:
                files.append(dirname + "/" + i)
                fnames.append(i)
        for index, i in enumerate(fnames):
            f = files[index]
            if str(star) in str(f):
                FOUND = False
                with open(f, 'r') as infile:
                    reader = csv.reader(infile, delimiter=",")
                    mapped_indices = {}
                    for row in reader:
                        if len(row) > 0:
                            if "liquid_0" in row[0]:
                                header = list(next(reader))
                                mapped_indices = self.__map_oxide_to_indices(header_row=header,
                                                                             oxides=all_oxides)
                                FOUND = True
                            elif FOUND:
                                for j in mapped_indices.keys():
                                    if j != "mass" and j != "temperature":
                                        d[j].append(((float(row[mapped_indices[j]]) / 100.0) *
                                                     float(row[mapped_indices["mass"]])))
                                    elif j == "temperature":
                                        d[j].append(float(row[mapped_indices[j]]))
                                    elif j == "mass":
                                        d[j].append(float(row[mapped_indices[j]]))
                        elif FOUND is True:
                            if len(row) == 0:
                                infile.close()
                                break
        return d
