import os
import csv
import pandas as pd
import matplotlib.pyplot as plt

bsp_chem_file = pd.read_csv("/Users/scotthull/Desktop/exoplanets/BSP_MORB_Compositions/adibekyan_bsp_compositions.csv")
morb_chem_file_1200 = pd.read_csv(
    "/Users/scotthull/Desktop/exoplanets/BSP_MORB_Compositions/adibekyan_morb_compositions_f1200.csv")
morb_chem_file_1400 = pd.read_csv(
    "/Users/scotthull/Desktop/exoplanets/BSP_MORB_Compositions/adibekyan_morb_compositions_f1400.csv")
morb_chem_file_1600 = pd.read_csv(
    "/Users/scotthull/Desktop/exoplanets/BSP_MORB_Compositions/adibekyan_morb_compositions_f1600.csv")

sun_bsp = {}
sun_morb_1200 = {}
sun_morb_1400 = {}
sun_morb_1600 = {}

for row in bsp_chem_file.index:
    if bsp_chem_file['Star'][row] == "Sun":
        print(row)
        sun_bsp = {
            "FeO": bsp_chem_file["FeO"][row],
            "Na2O": bsp_chem_file["Na2O"][row],
            "MgO": bsp_chem_file["MgO"][row],
            "Al2O3": bsp_chem_file["Al2O3"][row],
            "SiO2": bsp_chem_file["SiO2"][row],
            "CaO": bsp_chem_file["CaO"][row],
            "TiO2": bsp_chem_file["TiO2"][row],
            "Cr2O3": bsp_chem_file["Cr2O3"][row]
        }

for row in morb_chem_file_1200.index:
    if morb_chem_file_1200['Star'][row] == "Sun":
        print(row)
        sun_morb_1200 = {
            "FeO": morb_chem_file_1200["FeO"][row],
            "Na2O": morb_chem_file_1200["Na2O"][row],
            "MgO": morb_chem_file_1200["MgO"][row],
            "Al2O3": morb_chem_file_1200["Al2O3"][row],
            "SiO2": morb_chem_file_1200["SiO2"][row],
            "CaO": morb_chem_file_1200["CaO"][row],
            "TiO2": morb_chem_file_1200["TiO2"][row],
            "Cr2O3": morb_chem_file_1200["Cr2O3"][row]
        }

for row in morb_chem_file_1400.index:
    if morb_chem_file_1400['Star'][row] == "Sun":
        print(row)
        sun_morb_1400 = {
            "FeO": morb_chem_file_1400["FeO"][row],
            "Na2O": morb_chem_file_1400["Na2O"][row],
            "MgO": morb_chem_file_1400["MgO"][row],
            "Al2O3": morb_chem_file_1400["Al2O3"][row],
            "SiO2": morb_chem_file_1400["SiO2"][row],
            "CaO": morb_chem_file_1400["CaO"][row],
            "TiO2": morb_chem_file_1400["TiO2"][row],
            "Cr2O3": morb_chem_file_1400["Cr2O3"][row]
        }

for row in morb_chem_file_1600.index:
    if morb_chem_file_1600['Star'][row] == "Sun":
        print(row)
        sun_morb_1600 = {
            "FeO": morb_chem_file_1600["FeO"][row],
            "Na2O": morb_chem_file_1600["Na2O"][row],
            "MgO": morb_chem_file_1600["MgO"][row],
            "Al2O3": morb_chem_file_1600["Al2O3"][row],
            "SiO2": morb_chem_file_1600["SiO2"][row],
            "CaO": morb_chem_file_1600["CaO"][row],
            "TiO2": morb_chem_file_1600["TiO2"][row],
            "Cr2O3": morb_chem_file_1600["Cr2O3"][row]
        }

oxides = ["FeO", "SiO2", "MgO", "Na2O", "Al2O3", "CaO", "TiO2"]
nums = list(range(len(oxides)))

ax = plt.figure().add_subplot(111)
ax.plot(nums, [sun_bsp[i] for i in oxides], color="red", linewidth=2.0, label="BSP")
ax.plot(nums, [sun_morb_1200[i] for i in oxides], color="blue", linewidth=2.0, label="MORB F1200")
ax.plot(nums, [sun_morb_1400[i] for i in oxides], color="green", linewidth=2.0, label="MORB F1400")
ax.plot(nums, [sun_morb_1600[i] for i in oxides], color="pink", linewidth=2.0, label="MORB F1600")
ax.set_xticklabels(oxides)
ax.set_xlabel("Oxide")
ax.set_ylabel("Abundance (wt%)")
ax.grid()
ax.legend()

plt.show()
