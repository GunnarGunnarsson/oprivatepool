config = {
    'r': 500,
    't': lambda path: len(path) * 0.8,
    'ny': '-73.99,40.70,12',
    'data_folder': 'taxi-data-10k/complete',
    'data_filename_pattern': '%s/routes_green_tripdata_2015-*.json'
    #'data_folder': 'taxi-data/complete',
    #'data_filename_pattern': '%s/*small*.json'
}
