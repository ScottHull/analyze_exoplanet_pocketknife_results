import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

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

    def __init__(self, path):
        super().__init__()
        self.path = path

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

    def __quant_depletion(self, depleted_bsp_oxide, undepleted_bsp_oxide):
        return ((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0

    def __calc_depletion(self, undepleted_bsp_df, depleted_bsp_df):
        depletion_percentages = []

        for row in undepleted_bsp_df.index:
            star = undepleted_bsp_df['Star'][row]
            undepleted_bsp_feo = undepleted_bsp_df['FeO'][row]
            undepleted_bsp_na2o = undepleted_bsp_df['Na2O'][row]
            undepleted_bsp_mgo = undepleted_bsp_df['MgO'][row]
            undepleted_bsp_al2o3 = undepleted_bsp_df['Al2O3'][row]
            undepleted_bsp_sio2 = undepleted_bsp_df['SiO2'][row]
            undepleted_bsp_cao = undepleted_bsp_df['CaO'][row]
            undepleted_bsp_tio2 = undepleted_bsp_df['TiO2'][row]

            depleted_row = self.__get_depleted_row(star=star, depleted_df=depleted_bsp_df)
            if depleted_row is not None:
                depleted_bsp_feo = depleted_bsp_df['FeO'][row]
                depleted_bsp_na2o = depleted_bsp_df['Na2O'][row]
                depleted_bsp_mgo = depleted_bsp_df['MgO'][row]
                depleted_bsp_al2o3 = depleted_bsp_df['Al2O3'][row]
                depleted_bsp_sio2 = depleted_bsp_df['SiO2'][row]
                depleted_bsp_cao = depleted_bsp_df['CaO'][row]
                depleted_bsp_tio2 = depleted_bsp_df['TiO2'][row]

                depletion_feo = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_feo, depleted_bsp_oxide=depleted_bsp_feo)
                depletion_na2o = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_na2o, depleted_bsp_oxide=depleted_bsp_na2o)
                depletion_mgo = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_mgo, depleted_bsp_oxide=depleted_bsp_mgo)
                depletion_al2o3 = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_al2o3, depleted_bsp_oxide=depleted_bsp_al2o3)
                depletion_sio2 = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_sio2, depleted_bsp_oxide=depleted_bsp_sio2)
                depletion_cao = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_cao, depleted_bsp_oxide=depleted_bsp_cao)
                depletion_tio2 = self.__quant_depletion(undepleted_bsp_oxide=undepleted_bsp_tio2, depleted_bsp_oxide=depleted_bsp_tio2)

                depletion_pct = {
                    'feo': depletion_feo,
                    'na2o': depletion_na2o,
                    'mgo': depletion_mgo,
                    'al2o3': depletion_al2o3,
                    'sio2': depletion_sio2,
                    'cao': depletion_cao,
                    'tio2': depletion_tio2
                }

                depletion_percentages.append(depletion_pct)

        return depletion_percentages


    def plot_depletion(self):
        ax_sio2 = plt.figure().add_subplot(111)
        ax_feo = plt.figure().add_subplot(111)
        ax_mgo = plt.figure().add_subplot(111)
        ax_al2o3 = plt.figure().add_subplot(111)
        ax_na2o = plt.figure().add_subplot(111)
        adibekyan_depletion_f1400 = self.__calc_depletion(undepleted_bsp_df=self.adibekyan_bsp,
                                                          depleted_bsp_df=self.adibekyan_depleted_bsp_f1400)
        adibekyan_depletion_f1600 = self.__calc_depletion(undepleted_bsp_df=self.adibekyan_bsp,
                                                          depleted_bsp_df=self.adibekyan_depleted_bsp_f1600)
        kepler_depletion_f1400 = self.__calc_depletion(undepleted_bsp_df=self.kepler_bsp,
                                                          depleted_bsp_df=self.kepler_depleted_bsp_f1400)
        kepler_depletion_f1600 = self.__calc_depletion(undepleted_bsp_df=self.kepler_bsp,
                                                          depleted_bsp_df=self.kepler_depleted_bsp_f1600)
        
        sio2_depletion_f1400 = [i['sio2'] for i in adibekyan_depletion_f1400] + [i['sio2'] for i in
                                                                                 kepler_depletion_f1400]
        mgo_depletion_f1400 = [i['mgo'] for i in adibekyan_depletion_f1400] + [i['mgo'] for i in
                                                                                 kepler_depletion_f1400]
        feo_depletion_f1400 = [i['feo'] for i in adibekyan_depletion_f1400] + [i['feo'] for i in
                                                                                 kepler_depletion_f1400]
        na2o_depletion_f1400 = [i['na2o'] for i in adibekyan_depletion_f1400] + [i['na2o'] for i in
                                                                                 kepler_depletion_f1400]
        sio2_depletion_f1400 = [i['sio2'] for i in adibekyan_depletion_f1400] + [i['sio2'] for i in
                                                                                 kepler_depletion_f1400]
        al2o3_depletion_f1400 = [i['al2o3'] for i in adibekyan_depletion_f1400] + [i['al2o3'] for i in
                                                                                 kepler_depletion_f1400]

        sio2_depletion_f1600 = [i['sio2'] for i in adibekyan_depletion_f1600] + [i['sio2'] for i in
                                                                                 kepler_depletion_f1600]
        mgo_depletion_f1600 = [i['mgo'] for i in adibekyan_depletion_f1600] + [i['mgo'] for i in
                                                                               kepler_depletion_f1600]
        feo_depletion_f1600 = [i['feo'] for i in adibekyan_depletion_f1600] + [i['feo'] for i in
                                                                               kepler_depletion_f1600]
        na2o_depletion_f1600 = [i['na2o'] for i in adibekyan_depletion_f1600] + [i['na2o'] for i in
                                                                                 kepler_depletion_f1600]
        sio2_depletion_f1600 = [i['sio2'] for i in adibekyan_depletion_f1600] + [i['sio2'] for i in
                                                                                 kepler_depletion_f1600]
        al2o3_depletion_f1600 = [i['al2o3'] for i in adibekyan_depletion_f1600] + [i['al2o3'] for i in
                                                                                   kepler_depletion_f1600]
        
        ax_sio2.hist([sio2_depletion_f1400, sio2_depletion_f1600], bins=30, density=False, histtype='bar', rwidth=60,
                align='mid', label=['F1400', 'F1600'])
        ax_sio2.set_xlabel("Depletion % [((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0]")
        ax_sio2.set_ylabel("Number")
        ax_sio2.set_title("SiO2 Depletion")
        ax_sio2.grid()
        ax_sio2.legend()

        ax_feo.hist([feo_depletion_f1400, feo_depletion_f1600], bins=30, density=False, histtype='bar', rwidth=60,
                     align='mid', label=['F1400', 'F1600'])
        ax_feo.set_xlabel("Depletion % [((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0]")
        ax_feo.set_ylabel("Number")
        ax_feo.set_title("FeO Depletion")
        ax_feo.grid()
        ax_feo.legend()

        ax_mgo.hist([mgo_depletion_f1400, mgo_depletion_f1600], bins=30, density=False, histtype='bar', rwidth=60,
                     align='mid', label=['F1400', 'F1600'])
        ax_mgo.set_xlabel("Depletion % [((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0]")
        ax_mgo.set_ylabel("Number")
        ax_mgo.set_title("MgO Depletion")
        ax_mgo.grid()
        ax_mgo.legend()

        ax_al2o3.hist([al2o3_depletion_f1400, al2o3_depletion_f1600], bins=30, density=False, histtype='bar', rwidth=60,
                     align='mid', label=['F1400', 'F1600'])
        ax_al2o3.set_xlabel("Depletion % [((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0]")
        ax_al2o3.set_ylabel("Number")
        ax_al2o3.set_title("Al2O3 Depletion")
        ax_al2o3.grid()
        ax_al2o3.legend()

        ax_na2o.hist([na2o_depletion_f1400, na2o_depletion_f1600], bins=30, density=False, histtype='bar', rwidth=60,
                     align='mid', label=['F1400', 'F1600'])
        ax_na2o.set_xlabel("Depletion % [((depleted_bsp_oxide - undepleted_bsp_oxide) / undepleted_bsp_oxide) * 100.0]")
        ax_na2o.set_ylabel("Number")
        ax_na2o.set_title("Na2O Depletion")
        ax_na2o.grid()
        ax_na2o.legend()

        plt.show()


# i = Inspect(path="/Users/scotthull/Desktop/exoplanets/Depleted_Lithosphere_Compositions")
# i.plot_depletion()
