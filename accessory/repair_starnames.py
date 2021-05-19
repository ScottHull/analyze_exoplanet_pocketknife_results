import os
import csv

PATH = "/Users/scotthull/Desktop/exoplanets/Densities/Depleted_Lithosphere"

for dirname, dirnames, f in os.walk(PATH):
    for i in f:
        full_path = dirname + "/" + i
        if full_path.replace(".csv", "") + "_temp.csv" in os.listdir(dirname):
            os.remove(full_path.replace(".csv", "") + "_temp.csv")
        new_outfile = open(full_path.replace(".csv", "") + "_temp.csv", "w")
        c = csv.reader(open(full_path, 'r'), delimiter=",")
        for row in c:
            row[0] = row[0].replace(
                "_BSP_1400_HeFESTo_Input_File.txtHeFESTo_Output_File.txt",
                ""
            ).replace(
                "_BSP_1600_HeFESTo_Input_File.txtHeFESTo_Output_File.txt",
                ""
            ).replace(
                "_BSP_1200_HeFESTo_Input_File.txtHeFESTo_Output_File.txt",
                ""
            )
            row_str = ",".join(str(j) for j in row)
            new_outfile.write(row_str + "\n")
        new_outfile.close()
