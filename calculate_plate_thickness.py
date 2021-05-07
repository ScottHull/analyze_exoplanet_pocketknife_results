import csv
import os

path = "C:/Users/Scott/Desktop/3_26_2021/kepler/specific_buoyancy"

def get_buoyancy_file_metadata(fname):
    s = fname.split("_")
    name, bsp_temp, morb_ftemp, hefesto_starting_temp = s[0], s[2], s[4], s[5]
    return name, bsp_temp, morb_ftemp, hefesto_starting_temp.replace(".csv", "")

def read_buoyant_file(path, fname):
    with open(path + "/" + fname) as infile:
        reader = csv.reader(infile)
        return reader

def calc_min_plate_thickness(max_buoyancy):
    """
    The buoyant force on a plate is:
    F_b = t * int_0^d [ delta-rho * g ] dh
    where t is plate thickness, delta-rho is the density difference between BSP and MORB, g is grav, d is max depth,
    and dh is depth increment.

    Specific buoyant force is:
     F_b_s = F_b / t = int_0^d [ delta-rho * g ] dh
     F_b_s * t = F_b --> F_b < 0 = F_b_s * t < 0

    Therefore (because we want min depth where F_b < 0 (i.e. negative buoyancy)):
    :param max_buoyancy:
    :return:
    """
    pass

for i in os.listdir(path):
    name, bsp_temp, morb_ftemp, hefesto_starting_temp = get_buoyancy_file_metadata(fname=i)
    print(i, name, bsp_temp, morb_ftemp, hefesto_starting_temp)
    buoyancy_file = read_buoyant_file(path=path, fname=i)
    for row in buoyancy_file:
        star = row[0]
        max_buoyancy = row[-1]
