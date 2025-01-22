closest_dist_array = []

def dist_eqn(dist_1, dist_2):
    # TODO distance formula

def close_dist_finder(first_geo_array, second_geo_array):
    for i in first_geo_array:
        min_dist = float('inf')
        for j in second_geo_array:
            #TODO use dist def to get distance
            dist = dist_eqn(first_geo_array[i], second_geo_array[j])
            if dist < min_dist:
                min_dist = dist
                closest_dist_array[i] = second_geo_array[j]