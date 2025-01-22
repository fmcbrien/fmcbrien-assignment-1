import math

def dist_eqn(lat_1, lat_2, lon_1, lon_2):
    # TODO haversine distance formula
    # variables    
    R = 6371e3 # Earth's Radius
    phi_1 = lat_1 * math.pi/180
    phi_2 = lat_2 * math.pi/180
    del_phi = (lat_2-lat_1) * math.pi/180
    del_lambda = (lon_2-lon_1) * math.pi/180

    a = math.sin(del_phi/2)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(del_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c
    
    return dist

def close_dist_finder(first_geo_array, second_geo_array):
    closest_dist_array = []
    for location_1 in first_geo_array:
        min_dist = float('inf')
        for location_2 in second_geo_array:
            dist = dist_eqn(location_1[0], location_2[0], location_1[1], location_2[1])
            if dist < min_dist:
                min_dist = dist
                shortest_dist = location_2
        closest_dist_array.append(shortest_dist)

    return closest_dist_array

closest_array = close_dist_finder(geo_locations_1, geo_locations_2)
print(closest_array)
