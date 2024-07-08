import os
import time

import pandas as pd
import requests
from sklearn.model_selection import TimeSeriesSplit, train_test_split

API_KEY = None
URL = "api.akkio.com"
VERSION = "v1"
PROTOCOL = "https"
PORT = "443"


def partition_data(
    filename, out_location=os.getcwd(), test_partition=0.1, shuffle=True
):
    """Partition data to generate a train / test split"""

    fname = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    df = pd.read_csv(filename)

    training_data, testing_data = train_test_split(
        df, test_size=test_partition, shuffle=shuffle, random_state=25
    )

    print(f"No. of training examples: {training_data.shape[0]}")
    print(f"No. of testing examples: {testing_data.shape[0]}")

    train_filename = os.path.join(out_location, fname + "-train" + ext)
    test_filename = os.path.join(out_location, fname + "-test" + ext)

    training_data.to_csv(train_filename, index=False)
    testing_data.to_csv(test_filename, index=False)


def partition_time_series(
    filename, time_varname, response, out_location=os.getcwd(), n_splits=2, test_size=20
):
    """Partition time series data into training / test splits"""

    fname = os.path.splitext(filename)[0]
    ext = os.path.splitext(filename)[1]

    df = pd.read_csv(filename)

    df[time_varname] = pd.to_datetime(df[time_varname])
    df.set_index(time_varname, inplace=True)
    df.sort_index(inplace=True)

    tss = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

    X = df.drop(labels=[response], axis=1)
    y = df[response]

    for train_index, test_index in tss.split(X):
        X_train, X_test = X.iloc[train_index, :], X.iloc[test_index, :]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

    training_data = pd.concat([X_train, y_train], axis=1)
    testing_data = pd.concat([X_test, y_test], axis=1)

    train_filename = os.path.join(out_location, fname + "-train" + ext)
    test_filename = os.path.join(out_location, fname + "-test" + ext)

    training_data.to_csv(train_filename)
    testing_data.to_csv(test_filename)


# Import data from disk
def import_data(filepath):
    """
    Reads a file (CSV, Excel) into a Pandas DataFrame and then converts it to a list of dictionaries.

    :param filepath: str, path to the file
    :return: list of dicts, each dict representing a row in the DataFrame
    """

    # Mapping file extensions to Pandas functions
    file_readers = {
        ".csv": pd.read_csv,
        ".xlsx": pd.read_excel,
    }

    # Extract file extension and read the file
    file_extension = filepath.rsplit(".", 1)[-1].lower()
    read_function = file_readers.get("." + file_extension)

    if read_function:
        df = read_function(filepath, index_col=None)
    else:
        supported_types = ", ".join(file_readers.keys())
        raise ValueError(
            f"Unsupported file type '{file_extension}'. Supported file types are: {supported_types}."
        )

    # # Convert DataFrame to a list of dictionaries
    dict_list = df.to_dict(orient="records")

    # Make sure floats are converted to strings
    dict_list = [
        {k: (str(v) if isinstance(v, float) else v) for k, v in record.items()}
        for record in dict_list
    ]

    return dict_list


def add_rows_to_dataset(dataset_id, input_data):
    """
    Make API request to add rows to existing dataset

    Returns:
        dict: json response
    """
    start_time = time.time()
    response = requests.post(
        "{}://{}:{}/{}/datasets".format(PROTOCOL, URL, PORT, VERSION),
        json={"api_key": API_KEY, "id": dataset_id, "rows": input_data},
        timeout=120,
    )
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(
        f"Request to add rows to dataset {dataset_id} with {len(input_data)} samples completed in {elapsed_time:.4f} seconds."
    )

    return response.json()


def make_prediction(model_id, input_data, show_factors=False, save=False):
    """
    Make API request for inference on new data

    Returns:
        dict: json response
    """
    start_time = time.time()
    response = requests.post(
        "{}://{}:{}/{}/models".format(PROTOCOL, URL, PORT, VERSION),
        json={
            "api_key": API_KEY,
            "sample": True,
            "id": model_id,
            "data": input_data,
            "show_factors": show_factors,
        },
        timeout=120,
    )
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(
        f"Request to make predictions {model_id} with {len(input_data)} samples completed in {elapsed_time:.4f} seconds."
    )

    # Check for HTTP errors
    response.raise_for_status()

    # Parse JSON response
    resp_dict = response.json()

    # Check for application level errors
    if resp_dict.get("status") == "error":
        raise Exception(
            f"Error from API: {resp_dict.get('message', 'No error message provided')}"
        )

    if save:
        file_path = "predictions.csv"

        print(f"Saving prediction to disk to {file_path}")

        if "predictions" in resp_dict.keys():
            df = pd.DataFrame(resp_dict["predictions"])
        else:
            df = pd.DataFrame(resp_dict)

        df.to_csv(file_path, index=False)

        print("Done!")

    return resp_dict


if __name__ == "__main__":
    filename = "Lead_Scoring.csv"
    partition_data(filename)
