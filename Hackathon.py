from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

"""Parameters of interest:
Number of stars
Number of planets
Discovery method {Radial Velocity = 1, Imaging = 2, Eclipse Timing Variations = 3, Microlensing = 4, Transit = 5, Astrometry = 6, Transit Timing Variations = 7, Pulsar timing variations = 8, Pulsation timing variations = 9, Orbital brightness modulations = 10, Disk Kinematics = 11}
Orbital Period (days) **remove uncertainty**
Orbit semi-major axis (AU) **remove uncertainty**
Planet Radius (Earth radii) **remove uncertainty**
Planet mass (earth mass)  **remove uncertainty**
Eccentricity of orbit **remove uncertainty**
Insolation Flux (Earth flux) **remove uncertainty**
Equilibrium Temperature (K) **remove uncertainty**
Data shows transit timing variations? (0/1)
Spectral Type (encode in table with only binary)    df = pd.DataFrame({'spectral_type': ['G2V', 'K1V', 'M3V', 'G2V']})  //df_encoded = pd.get_dummies(df, columns=['spectral_type'])
Stellar effective temp (k) **remove uncertainty**
Stellar Radius (sun Radius) **remove uncertainty**
Stellar Mass (sun Mass)  **remove uncertainty**
Stellar Metallicity Ratio (need to convert to integer??)
Stellar Surface Gravity **remove uncertainty**



"""

X, y = make_classification(n_samples=1000, n_features=4,
                           n_informative=2, n_redundant=0,
                           random_state=0, shuffle=False)
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)
print(clf.predict([[0, 0, 0, 0]]))