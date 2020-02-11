# Define a basic Haversine distance formula
# reference: https://gist.githubusercontent.com/s-heisler/e1548f31319dee864d8c5c522be06760/raw/4df8d2d9f43641c25879346a7fc06953fcaf35cb/haversine_function.py
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    KM = 6372.8
    lat1, lon1, lat2, lon2 = map(np.deg2rad, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    total_km = KM * c
    return total_km
