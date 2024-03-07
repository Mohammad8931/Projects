import json
import pickle
import numpy as np

# Initialize global variables to hold locations, data columns, and the trained model.
__locations = None
__data_columns = None
__model = None


def get_estimated_price(location, sqft, bedrooms, bath):
    # Try to find the index of the specified location in the data columns.
    # If not found, loc_index is set to -1.
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    # Create a numpy array with zeros, length equal to the number of columns.
    x = np.zeros(len(__data_columns))
    # Assign input parameters to the appropriate indices.
    x[0] = sqft  # Square footage
    x[1] = bath  # Number of bathrooms
    x[2] = bedrooms  # Number of bedrooms
    if loc_index >= 0:
        x[loc_index] = 1  # Set location index to 1 if the location is found.

    # Use the model to predict the price based on the input vector x, and round the result.
    return round(__model.predict([x])[0], 2)


def get_location_names():
    # Return the list of location names loaded into __locations.
    return __locations


def load_saved_artifacts():
    # Load the saved model and column data from disk.
    print("Loading saved artifacts...start")
    global __data_columns, __locations, __model

    # Load data columns and locations from columns.json.
    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # Assume location data starts from the 4th column.

    # Load the trained model from the .pickle file.
    with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
        __model = pickle.load(f)


# Test the functions if this script is executed directly.
if __name__ == '__main__':
    load_saved_artifacts()  # Load model and column names.
    print(get_location_names())  # Print list of locations.
    # Example predictions.
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
