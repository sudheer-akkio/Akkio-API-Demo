# Setup
import akkio

import utils

API_KEY = "463c3703-cb1d-434b-a540-bbcb4b5db0d7"
akkio.api_key = API_KEY
utils.API_KEY = API_KEY

# Show all available datasets
# datasets = akkio.get_datasets()
# print(datasets)

# Show selected dataset by id
# dataset_id = "T2GLrINFpxRGx9ME1A2M"  # Found in Akkio datasets tab
# selected_dataset = [ds for ds in datasets["datasets"] if ds["id"] == dataset_id]
# print(selected_dataset)

# Import train data
train_filepath = "Lead_Scoring-train.csv"
train_data = utils.import_data(train_filepath)

# Create a new empty dataset
new_dataset = akkio.create_dataset("lead scoring api test 3")
print(new_dataset)

dataset_id = new_dataset["dataset_id"]

# Add rows to new dataset
response = utils.send_dataset_api_request(dataset_id, train_data)
print(response)

# Import test data
# test_filepath = "test_data.csv"
# test_data = import_data(test_filepath)

# Add rows to existing dataset
# dataset_id = "NRbO45XKbglMwNVmczZl"
# response = send_api_request(dataset_id, test_data)
# print(response)
