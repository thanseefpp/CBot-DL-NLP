import tensorflow as tf
from model.chatbot_database import create_table,find_parent
from datetime import datetime
import json


#file path of the dataset
file_path = "Dataset/RC_2015-01"


def format_data(data):
    # This will format the data contain (\n,\r,single quote - double quote)
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data


if __name__ == "__main__":
    # This will create a sql lite table.
    create_table()
    row_counter = 0
    paired_rows = 0
    
    # Here this will open the file and extract the data.
    with open(file_path,buffering=1000) as f:
        for row in f:
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            parent_data = find_parent(parent_id)
            # print(parent_data)