import os
import time

import pandas as pd
import requests
from sklearn.model_selection import train_test_split

API_KEY = None
BASE_URL = "api.akkio.com/api"
URL = "api.akkio.com"
VERSION = "v1"
PROTOCOL = "https"
ENDPOINT = "chat-explore"
PORT = "443"


# Chat Wrappers
def create_chat_request(project_id, content):
    """
    Make API request for chat creation

    Returns:
        dict: json response
    """

    MODE = "new"

    url = f"{PROTOCOL}://{BASE_URL}/{VERSION}/{ENDPOINT}/{MODE}"
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    data = {
        "project_id": project_id,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=120,
    )

    # Check for HTTP errors
    response.raise_for_status()

    return response.json()


def check_task_status(task_id):
    """
    Check task status from Chat creation POST call

    Returns:
        dict: json response
    """

    MODE = "status"

    url = f"{PROTOCOL}://{BASE_URL}/{VERSION}/{ENDPOINT}/{MODE}/{task_id}"
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}

    response = requests.get(
        url,
        headers=headers,
        timeout=120,
    )

    # Check for HTTP errors
    response.raise_for_status()

    return response.json()


def get_chat_results(chat_id, format_type="plotly_json"):
    """
    Get chat results based on chat_id

    Returns:
        dict: json response
    """

    # BASE64_PNG = "base64_png"
    # PLOTLY_JSON = "plotly_json"

    MODE = "chats"

    url = f"{PROTOCOL}://{BASE_URL}/{VERSION}/{ENDPOINT}/{MODE}/{chat_id}"
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    query_params = {"image_format": format_type}

    response = requests.get(
        url,
        headers=headers,
        params=query_params,
        timeout=120,
    )

    # Check for HTTP errors
    response.raise_for_status()
    return response.json()


# Import data from disk
def import_data(filepath):
    """
    Reads a file (CSV, Excel) into a Pandas DataFrame.

    :param filepath: str, path to the file
    :return: DataFrame
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
        err_msg = f"Unsupported file type '{file_extension}'. Supported file types are: {supported_types}."
        print(err_msg)
        raise ValueError(err_msg)

    return df


def df_to_dict(df):
    """
    Converts DataFrame to list of dictionaries
    """
    # Convert all data in the DataFrame to strings (force conversion to string since
    # we implicitely cast to the correct DType when generating the dataset view)
    df = df.applymap(str)

    # Convert DataFrame to a list of dictionaries
    dict_list = df.to_dict(orient="records")

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


def create_project(project_name, owner_id, org_id):
    """
    Make API request for create project

    Returns:
        dict: json response
    """

    url = f"{PROTOCOL}://{BASE_URL}/{VERSION}/projects"
    headers = {"X-Api-Key": API_KEY, "Content-Type": "application/json"}
    data = {
        "name": project_name,
        "_owner": owner_id,
        "_org": org_id,
    }

    response = requests.post(
        url,
        json=data,
        headers=headers,
        timeout=120,
    )

    # Check for HTTP errors
    response.raise_for_status()

    return response.json()


def make_prediction(
    model_id,
    input_data,
    show_factors=False,
    save=False,
    save_file_path="",
):
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
        if not save_file_path:
            save_file_path = "predictions.csv"

        print(f"Saving prediction to disk to {save_file_path}")

        if "predictions" in resp_dict.keys():
            df = pd.DataFrame(resp_dict["predictions"])
        else:
            df = pd.DataFrame(resp_dict)

        df.to_csv(save_file_path, index=False)

        print("Done!")

    return resp_dict


def set_dataset_fields(dataset_id, fields):
    """
    Make API request to set dataset fields

    Returns:
        dict: json response
    """

    # filed column type options are below
    # - category
    # - id
    # - integer
    # - float
    # - string
    # - date
    # - unknown (maps to disabled)

    # input data must look like this
    # fields = [
    #     {
    #         'name': {column1_name},
    #         'type': {column1_type},
    #         'valid': true
    #     },
    #     {
    #         'name': {column2_name},
    #         'type': {column2_type},
    #         'valid': true
    #     },
    #     ...
    # ]

    start_time = time.time()
    response = requests.post(
        "{}://{}:{}/{}/datasets".format(PROTOCOL, URL, PORT, VERSION),
        json={"api_key": API_KEY, "id": dataset_id, "fields": fields},
        timeout=120,
    )
    end_time = time.time()

    elapsed_time = end_time - start_time

    print(
        f"Request to set dataset fields in {dataset_id} completed in {elapsed_time:.4f} seconds."
    )

    return response.json()
