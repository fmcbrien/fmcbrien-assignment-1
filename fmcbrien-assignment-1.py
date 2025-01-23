import math

'''
Name: Fallon McBrien
Email: fmcbrien@bu.edu
EC530

Assuming location arrays are formatted such that each row has two col inputs, lat and lon respectively

Ex.: geo_locations_1 = [[lat1, lon1], [lat2, lon2], ...]

This program uses the Haversine Distance Formula to find the closest GPS location in the second array of
locations to the GPS locations in the first array. The distance formula was taken from the following
website: https://www.movable-type.co.uk/scripts/latlong.html
'''

def dist_eqn(lat_1, lat_2, lon_1, lon_2):
    # using Haversine distance formula for distance between two GPS points

    # variables for the formula
    R = 6371e3 # Earth's Radius
    phi_1 = lat_1 * math.pi/180
    phi_2 = lat_2 * math.pi/180
    del_phi = (lat_2-lat_1) * math.pi/180
    del_lambda = (lon_2-lon_1) * math.pi/180

    # formula implementation
    a = math.sin(del_phi/2)**2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(del_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = R * c
    
    return dist

def close_dist_finder(first_geo_array, second_geo_array):
    # nested for loop to compare each value in the first GPS location array to each value in the second
    closest_dist_array = []
    for location_1 in first_geo_array:
        # set initial minimum distance to infinity so there will always be a min dist as long as there is a location in array 1 and 2
        min_dist = float('inf')
        for location_2 in second_geo_array:
            dist = dist_eqn(location_1[0], location_2[0], location_1[1], location_2[1])
            # determines if the distance of the current point in array 2 is closer than the previous closest distance calculated
            if dist < min_dist:
                min_dist = dist
                shortest_dist = location_2

        print("The closest location to ", location_1, "is ", min_dist/1000, "kms away at point", shortest_dist)
        closest_dist_array.append(shortest_dist)

    print("The array of distances closest to the respective index location in the first array is ", closest_dist_array)

    return closest_dist_array

# # Example implementation of the code where geo_locations_x is an array of GPS locations
# closest_array = close_dist_finder(geo_locations_1, geo_locations_2)
# print(closest_array)
