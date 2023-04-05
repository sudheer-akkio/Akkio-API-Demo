
import akkio
akkio.api_key = '463c3703-cb1d-434b-a540-bbcb4b5db0d7'

models = akkio.get_models()['models']
for model in models:
    print(model)
print(f"Number of models: {len(models)}\n")

# Find correct model
model_name = "Mobile Price Classification"
selected_model  = [model for model in models if model['name'] == model_name]
print(f"Model: {selected_model}\n")

# Why are there multiple datasets and how can figure out which one is the most up to date?
datasets = akkio.get_datasets()['datasets']
for ds in datasets:
    print(ds)

print(f"Num Dataset: {len(datasets)}\n")

dataset_name = "train.csv"

# training_dataset = akkio.get_dataset(dataset_id) # There's no get_dataset method???
training_dataset = [dataset for dataset in datasets if dataset['name'] == dataset_name]
print(training_dataset[0])

dataset_id = training_dataset[0]['id']

# create a model
print("Creating model....")
new_model = akkio.create_model(dataset_id, ['price_range'], [], {'duration': 1})
print("Completed!")

for key,val in new_model.items():
    print(key)
    print(val)
    print("\n")

# Create dummy data
# new_data = []
# new_data.append({"ram":"2549","px_width":"756","px_height":"20","int_memory":"7"})
# new_data.append({"ram":"2600","px_width":"600","px_height":"10","int_memory":"4"})

# # Predictions
# prediction = akkio.make_prediction(selected_model[0]['id'], new_data, explain=True)
# print(prediction['predictions'][0])