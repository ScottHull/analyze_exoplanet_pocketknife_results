import os
import pandas as pd


class CorrectComposition:

    asplund_na = 1479108.388
    asplund_si = 32359365.69
    asplund_fe = 28183829.31
    asplund_sivsfe = asplund_si / asplund_fe
    asplund_navsfe = asplund_na / asplund_fe

    mcd_earth_fe = 29.6738223341739
    mcd_earth_na = 0.40545783900173
    mcd_earth_si = 29.6859892035662

    mcd_sivsfe = mcd_earth_si / mcd_earth_fe
    mcd_navsfe = mcd_earth_na / mcd_earth_fe

    adjust_si = mcd_sivsfe / asplund_sivsfe
    adjust_na = mcd_navsfe / asplund_navsfe

    def __init__(self, path_to_file, name):
        self.path = path_to_file
        try:
            os.remove(name)
        except:
            pass
        self.outfile = open(name, 'w')
        self.na_correction = self.adjust_na
        self.si_correction = self.adjust_si

    def correct_compositions(self):
        df = pd.read_csv(self.path)
        headers = list(df.keys())
        header_str = ",".join(str(i) for i in headers)
        self.outfile.write(header_str + "\n")
        for row in df.index:
            s = 0
            correct_si = None
            correct_na = None
            reformatted = [df["Star"][row]]
            for element in headers:
                if element != "Star":
                    if element == "Si":
                        s += df[element][row] * self.si_correction
                        correct_si = df[element][row] * self.si_correction
                    elif element == "Na":
                        s += df[element][row] * self.na_correction
                        correct_na = df[element][row] * self.na_correction
                    else:
                        s += df[element][row]
            for element in headers:
                if element != "Star":
                    if element == "Si":
                        reformatted.append(correct_si / s * 100.0)
                    elif element == "Na":
                        reformatted.append(correct_na / s * 100.0)
                    else:
                        reformatted.append(df[element][row] / s * 100.0)
            row_str = ",".join(str(i) for i in reformatted)
            self.outfile.write(row_str + "\n")
        self.outfile.close()



CorrectComposition(
    path_to_file="/Users/scotthull/Desktop/kepler_star_compositions.csv",
    name="/Users/scotthull/Desktop/kepler_si_na_corrected_star_compositions.csv"
).correct_compositions()

