class _AtomicWeights:

    def __init__(self):
        self.fe = 55.845
        self.mg = 24.305
        self.si = 28.086
        self.ca = 40.078
        self.al = 26.982
        self.ti = 47.867
        self.na = 22.99
        self.o = 15.99


class _OxideCationNumbers:

    def __init__(self):
        self.fe = 1  # feo, 1
        self.mg = 1  # mgo, 1
        self.si = 1  # sio2, 1
        self.ca = 1  # cao, 1
        self.al = 2  # al2o3, 2
        self.ti = 1  # tio2, 1
        self.na = 2  # na2o, 2


class _OxideWeights:

    def __init__(self):
        self.atomic_weights = _AtomicWeights()
        self.oxide_cation_numbers = _OxideCationNumbers()
        self.feo = (self.atomic_weights.fe * self.oxide_cation_numbers.fe) + self.atomic_weights.o
        self.mgo = (self.atomic_weights.mg * self.oxide_cation_numbers.mg) + self.atomic_weights.o
        self.sio2 = (self.atomic_weights.si * self.oxide_cation_numbers.si) + (self.atomic_weights.o * 2)
        self.cao = (self.atomic_weights.ca * self.oxide_cation_numbers.ca) + self.atomic_weights.o
        self.al2o3 = (self.atomic_weights.al * self.oxide_cation_numbers.al) + (self.atomic_weights.o * 3)
        self.tio2 = (self.atomic_weights.ti * self.oxide_cation_numbers.ti) + (self.atomic_weights.o * 2)
        self.na2o = (self.atomic_weights.na * self.oxide_cation_numbers.na) + self.atomic_weights.o


class Convert:

    def __init__(self):
        self.atomic_weights = _AtomicWeights()
        self.oxide_cation_numbers = _OxideCationNumbers()
        self.oxide_weights = _OxideWeights()

    def convert_oxide_pct_to_cation_pct(self, oxides):
        given_feo = oxides['feo']
        given_mgo = oxides['mgo']
        given_sio2 = oxides['sio2']
        given_cao = oxides['cao']
        given_al2o3 = oxides['al2o3']
        given_tio2 = oxides['tio2']
        given_na2o = oxides['na2o']

        moles_feo = given_feo / self.oxide_weights.feo
        moles_mgo = given_mgo / self.oxide_weights.mgo
        moles_sio2 = given_sio2 / self.oxide_weights.sio2
        moles_cao = given_cao / self.oxide_weights.cao
        moles_al2o3 = given_al2o3 / self.oxide_weights.al2o3
        moles_tio2 = given_tio2 / self.oxide_weights.tio2
        moles_na2o = given_na2o / self.oxide_weights.na2o

        moles_fe = moles_feo * self.oxide_cation_numbers.fe
        moles_mg = moles_mgo * self.oxide_cation_numbers.mg
        moles_si = moles_sio2 * self.oxide_cation_numbers.si
        moles_ca = moles_cao * self.oxide_cation_numbers.ca
        moles_al = moles_al2o3 * self.oxide_cation_numbers.al
        moles_ti = moles_tio2 * self.oxide_cation_numbers.ti
        moles_na = moles_na2o * self.oxide_cation_numbers.na
        s = moles_fe + moles_mg + moles_si + moles_ca + moles_al + moles_ti + moles_na

        mol_pct_fe = (moles_fe / s) * 100.0
        mol_pct_mg = (moles_mg / s) * 100.0
        mol_pct_si = (moles_si / s) * 100.0
        mol_pct_ca = (moles_ca / s) * 100.0
        mol_pct_al = (moles_al / s) * 100.0
        mol_pct_ti = (moles_ti / s) * 100.0
        mol_pct_na = (moles_na / s) * 100.0

        return {
            'fe': mol_pct_fe,
            'mg': mol_pct_mg,
            'si': mol_pct_si,
            'ca': mol_pct_ca,
            'al': mol_pct_al,
            'ti': mol_pct_ti,
            'na': mol_pct_na
        }
