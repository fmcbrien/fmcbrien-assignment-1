import math
import pandas as pd
import re

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
    overall_min_dist = float('inf')
    overall_shortest_pair = None

    for location_1 in first_geo_array:
        # set initial minimum distance to infinity so there will always be a min dist as long as there is a location in array 1 and 2
        min_dist = float('inf')
        shortest_dist = None
        for location_2 in second_geo_array:
            dist = dist_eqn(location_1[0], location_2[0], location_1[1], location_2[1])
            # determines if the distance of the current point in array 2 is closer than the previous closest distance calculated
            if dist < min_dist:
                min_dist = dist
                shortest_dist = location_2

            if dist < overall_min_dist:
                overall_min_dist = dist
                overall_shortest_pair = (location_1, location_2)

        print("The closest location to ", location_1, "is", min_dist/1000, "kms away at point", shortest_dist)
        closest_dist_array.append(shortest_dist)

    print("The array of distances closest to the respective index location in the first array is", closest_dist_array)

    # Show the overall shortest distance
    overall_distance_km = overall_min_dist / 1000
    print(f"\nOverall shortest distance is {overall_distance_km:.2f} kms between {overall_shortest_pair[0]} and {overall_shortest_pair[1]}.")

    return closest_dist_array

def preprocess_csv_data(data):
    # Remove any characters that are not valid decimal points or digits
    return re.sub(r"[^\d\.\-]", "", data)

def read_csv_locations(file_name, col_names):
    try:
        # Read CSV using pandas from either local file or URL
        df = pd.read_csv(file_name)
    except Exception as e:
        raise ValueError(f"Error reading the CSV file: {e}")
    
    # Check if required columns exist
    for col in col_names:
        if col.strip() not in df.columns:
            raise ValueError(f"Column '{col}' does not exist in the CSV file.")
    
    geolocations = []
    for _, row in df.iterrows():
        # Preprocess latitude and longitude
        lat = preprocess_csv_data(str(row[col_names[0].strip()]))
        lon = preprocess_csv_data(str(row[col_names[1].strip()]))
        geolocations.append((float(lat), float(lon)))
        
    return geolocations

def get_input_type(prompt):
    while True:
        file_type = input(prompt).strip().lower()
        if file_type in ["manual", "csv"]:
            return file_type
        else:
            print("Invalid file type input. Please enter 'manual' or 'csv'.")

def is_lat_lon(lat, lon):
    lat_range = re.compile(r"^-?(90(\.0+)?|[0-8]?\d(\.\d+)?)$")
    lon_range = re.compile(r"^-?(180(\.0+)?|1[0-7]\d(\.\d+)?|[0-9]?\d(\.\d+)?)$")
    return lat_range.match(lat) and lon_range.match(lon)

def get_manual_locations(prompt):
    while True:
        try:
            locations = input(prompt).split()
            geo_locations = []
            for location in locations:
                lat, lon = location.split(",")
                if is_lat_lon(lat.strip(), lon.strip()):
                    geo_locations.append((float(lat.strip()), float(lon.strip())))
                else:
                    print(f"Invalid input for location: {location}. Please enter in 'latitude,longitude' format.")
                    break
            else:
                return geo_locations  # Return if all locations are valid
        except ValueError:
            print("Invalid format. Please ensure you enter locations as 'latitude,longitude' (e.g., '34.0,-58.0' or '-34.0,-58.0').")

def get_csv_locations(prompt):
    while True:
        file_name = input(prompt)
        column_names = input("Enter the column names (e.g., 'latitude,longitude'): ").split(",")
        try:
            return read_csv_locations(file_name, column_names)
        except (FileNotFoundError, ValueError):
            print("Error reading the file or invalid format. Please try again.")

def main():
    print("For the first location array:")
    file_type_1 = get_input_type("Please enter the file type (manual, csv): ")
    
    if file_type_1 == "manual":
        geo_locations_1 = get_manual_locations("Enter your first array (latitude,longitude latitude,longitude ...): ")
    else:  # file_type_1 == "csv"
        geo_locations_1 = get_csv_locations("Enter the name of your CSV file: ")

    print("\nFor the second location array:")
    file_type_2 = get_input_type("Please enter the file type (manual, csv): ")

    if file_type_2 == "manual":
        geo_locations_2 = get_manual_locations("Enter your second array (latitude,longitude latitude,longitude ...): ")
    else:  # file_type_2 == "csv"
        geo_locations_2 = get_csv_locations("Enter the name of your CSV file: ")

    closest_array = close_dist_finder(geo_locations_1, geo_locations_2)
    print(closest_array)

if __name__ == "__main__":
    main()