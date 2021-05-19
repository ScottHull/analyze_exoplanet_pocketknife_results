import pandas as pd
import numpy as np
from math import isnan
import matplotlib.pyplot as plt
from src.atomic import Convert
from sklearn import linear_model
import statsmodels.api as sm

# BSP temperature, MORB F temperature, MORB temperature
runs = [
    (1600, 1600, 1600),
    (1600, 1600, 1400),
    (1600, 1400, 1400),
    (1400, 1400, 1400),
]


def get_cation_pct(star, composition):
    given_feo = composition['FeO'][star]
    given_mgo = composition['MgO'][star]
    given_sio2 = composition['SiO2'][star]
    given_cao = composition['CaO'][star]
    given_al2o3 = composition['Al2O3'][star]
    given_tio2 = composition['TiO2'][star]
    given_na2o = composition['Na2O'][star]
    oxides = {
        "feo": given_feo,
        "mgo": given_mgo,
        "sio2": given_sio2,
        "cao": given_cao,
        "al2o3": given_al2o3,
        "tio2": given_tio2,
        "na2o": given_na2o
    }
    atomic_pct = Convert().convert_oxide_pct_to_cation_pct(oxides=oxides)
    return atomic_pct


def get_composition_file(path_to_folder, material, F_temperature, runs=None):
    df = None
    if runs is None:
        runs = ["kepler", "adibekyan"]
    for index, run in enumerate(runs):
        bsp_template = path_to_folder + "/{}_{}_Compositions.csv".format(run.lower(), material.upper())
        morb_template = path_to_folder + "/{}_f{}_{}_Compositions.csv".format(run.lower(), F_temperature,
                                                                              material.upper())
        selected = None
        if material.lower() == "bsp":
            selected = bsp_template
        else:
            selected = morb_template
        if index == 0:
            df = pd.read_csv(selected)
            df['run'] = ['kepler' for i in range(0, len(list(df['Star'])))]
            df.set_index('Star', inplace=True)
        else:
            df2 = pd.read_csv(selected)
            df2['run'] = ['adibekyan' for i in range(0, len(list(df2['Star'])))]
            df2.set_index('Star', inplace=True)
            df2 = df2.drop("Sun")
            df = df.append(df2)
    return df


def get_density_file(path_to_folder, bsp_temperature, morb_F_temperature, morb_temperature, runs=None):
    df = None
    if runs is None:
        runs = ["kepler", "adibekyan"]
    for index, run in enumerate(runs):
        template = path_to_folder + "/{}_BSP_{}_MORB_F{}_{}.csv".format(run.capitalize(), bsp_temperature,
                                                                        morb_F_temperature, morb_temperature)
        if index == 0:
            df = pd.read_csv(template)
            df.set_index('star', inplace=True)
        else:
            df2 = pd.read_csv(template)
            df2.set_index('star', inplace=True)
            df2 = df2.drop("Sun")
            df = df.append(df2)
    return df


def get_data(element_1, element_2, composition, density, bsp_temp, morb_f_temp, morb_temp):
    data = []
    for star in composition.index:
        if star in density.index.values.tolist():
            run = composition['run'][star]
            element_1 = element_1[0:2].lower()
            element_2 = element_2[0:2].lower()
            cation_pct = get_cation_pct(star=star, composition=composition)
            element_1_val = cation_pct[element_1]
            element_2_val = cation_pct[element_2]
            s = sum(list(cation_pct.values()))
            try:
                final_density = density["573.68"][star].values[0]
            except:
                final_density = density["573.68"][star]
            if not isnan(float(final_density)):
                data.append((star, run, bsp_temp, morb_f_temp, morb_temp, element_1_val, element_2_val, final_density))
    return data


def reformat_data(data, element_1, element_2):
    element_1 = element_1[0:2].lower()
    element_2 = element_2[0:2].lower()
    d = {
        'bsp_temp': [i[2] for i in data],
        'morb_f_temp': [i[3] for i in data],
        'morb_temp': [i[4] for i in data],
        '{}/{}'.format(element_1, element_2): [i[5] / i[6] for i in data],
        'final_density': [i[7] for i in data]
    }
    df = pd.DataFrame(d)
    print(df)
    return df


def regression(df, element_1, element_2, regression_headers_x):
    element_1 = element_1[0:2].lower()
    element_2 = element_2[0:2].lower()
    print("X: ", regression_headers_x)
    X = df[regression_headers_x]
    Y = df['final_density']
    # with sklearn
    regr = linear_model.LinearRegression()
    regr.fit(X, Y)
    print('Intercept: \n', regr.intercept_)
    print('Coefficients: \n', regr.coef_)
    X = sm.add_constant(X)  # adding a constant
    model = sm.OLS(Y, X).fit()
    predictions = model.predict(X)
    print_model = model.summary()
    print(print_model)
    d = {}
    for index, i in enumerate(regression_headers_x):
        d.update({i: regr.coef_[index]})
    return d, regr.intercept_


def predict(intercept, x_variables, input_df, coefficients):
    y = []
    for row in input_df.index:
        s = 0
        for i in x_variables:
            coeff = coefficients[i]
            val = input_df[i][row]
            s += coeff * val
        y.append(s + intercept)
    return y


composition_path = "C:/Users/Scott/Desktop/3_26_2021/summary"
density_path = composition_path + "/specific_buoyancy"
element_1 = "SiO2"
element_2 = "FeO"

element_1_cation = element_1[0:2].lower()
element_2_cation = element_2[0:2].lower()
# regression_dependent_variables = ['bsp_temp', 'morb_f_temp', 'morb_temp',
#                                   '{}/{}'.format(element_1_cation, element_2_cation)]
regression_dependent_variables = ['{}/{}'.format(element_1_cation, element_2_cation)]

all_bsp_data = []
all_morb_data = []

c_bsp = get_composition_file(path_to_folder=composition_path, material="bsp", F_temperature="")
for index, r in enumerate(runs):
    bsp_temp, morb_f_temp, morb_temp = r[0], r[1], r[2]
    c_morb = get_composition_file(path_to_folder=composition_path, material="morb", F_temperature=morb_f_temp)
    d = get_density_file(path_to_folder=density_path, bsp_temperature=bsp_temp,
                         morb_F_temperature=morb_f_temp, morb_temperature=morb_temp)
    data_bsp = get_data(element_1=element_1, element_2=element_2, composition=c_bsp, density=d, bsp_temp=bsp_temp,
                        morb_f_temp=morb_f_temp, morb_temp=morb_temp)
    data_morb = get_data(element_1=element_1, element_2=element_2, composition=c_morb, density=d, bsp_temp=bsp_temp,
                         morb_f_temp=morb_f_temp, morb_temp=morb_temp)
    all_bsp_data.append(data_bsp)
    all_morb_data.append(data_morb)

all_bsp_data = [item for sublist in all_bsp_data for item in sublist]
all_morb_data = [item for sublist in all_morb_data for item in sublist]

reform_df_bsp = reformat_data(data=all_bsp_data, element_1=element_1, element_2=element_2)
reform_df_morb = reformat_data(data=all_morb_data, element_1=element_1, element_2=element_2)
bsp_coeffs, bsp_intercept = regression(df=reform_df_bsp, element_1=element_1, element_2=element_2,
                                       regression_headers_x=regression_dependent_variables)
morb_coeffs, morb_intercept = regression(df=reform_df_morb, element_1=element_1, element_2=element_2,
                                         regression_headers_x=regression_dependent_variables)
bsp_model = predict(intercept=bsp_intercept, input_df=reform_df_bsp, coefficients=bsp_coeffs,
                    x_variables=regression_dependent_variables)
morb_model = predict(intercept=morb_intercept, input_df=reform_df_morb, coefficients=morb_coeffs,
                     x_variables=regression_dependent_variables)

fig = plt.figure(figsize=(16, 9))
ax = fig.add_subplot(111)
ax.scatter(
    [i[5] / i[6] for i in all_bsp_data],
    [i[7] for i in all_bsp_data],
    marker="+",
    color='black',
    label='dataset'
)
ax.scatter(
    [i[5] / i[6] for i in all_bsp_data],
    bsp_model,
    marker="+",
    color='red',
    label='model'
)
ax.set_xlabel('{}/{} (cation %)'.format(element_1_cation, element_2_cation))
ax.set_ylabel("Specific Buoyancy @ 573.68 km")
ax.set_title("BSP")
ax.grid()
ax.legend()

fig2 = plt.figure(figsize=(16, 9))
ax2 = fig2.add_subplot(111)
ax2.scatter(
    [i[5] / i[6] for i in all_morb_data],
    [i[7] for i in all_morb_data],
    marker="+",
    color='black',
    label='dataset'
)
ax2.scatter(
    [i[5] / i[6] for i in all_morb_data],
    morb_model,
    marker="+",
    color='red',
    label='model'
)
ax2.set_xlabel('{}/{} (cation %)'.format(element_1_cation, element_2_cation))
ax2.set_ylabel("Specific Buoyancy @ 573.68 km")
ax2.set_title("MORB")
ax2.grid()
ax2.legend()

plt.show()
