import tensorflow as tf
from model.chatbot_database import create_table,find_parent,find_existing_score,\
    sql_insert_replace_comment,sql_insert_has_parent,sql_insert_no_parent,remove_parent_null_table_data
from datetime import datetime
import json

#file path of the dataset
file_path = "Dataset/RC_2015-01"

start_row = 0
end_row = 1000000

def format_data(data):
    # This will format the data contain (\n,\r,single quote - double quote)
    data = data.replace('\n',' newlinechar ').replace('\r',' newlinechar ').replace('"',"'")
    return data

def acceptable_data(data):
    if len(data.split(' ')) > 1000 or len(data) < 1:
        return False
    elif len(data) > 32000:
        return False
    elif data == '[deleted]':
        return False
    elif data == '[removed]':
        return False
    else:
        return True

if __name__ == "__main__":
    # This will create a sql lite table.
    create_table()
    row_counter = 0
    paired_rows = 0
    # Here this will open the file and extract the data.
    with open(file_path,buffering=1000) as f:
        for row in f:            
            row_counter += 1
            if row_counter > start_row:
                try:
                    row = json.loads(row)
                    parent_id = row['parent_id'].split('_')[1]
                    body = format_data(row['body'])
                    created_utc = row['created_utc']
                    score = row['score']
                    comment_id = row['id']
                    subreddit = row['subreddit']
                    parent_data = find_parent(parent_id)
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            if acceptable_data(body):
                                sql_insert_replace_comment(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                
                    else:
                        if acceptable_data(body):
                            if parent_data:
                                if score >= 2:
                                    sql_insert_has_parent(comment_id,parent_id,parent_data,body,subreddit,created_utc,score)
                                    paired_rows += 1
                            else:
                                sql_insert_no_parent(comment_id,parent_id,body,subreddit,created_utc,score)
                except Exception as e:
                    print(e)
                    
            if row_counter % 100000 == 0:
                    print(f"Row Counter Value {row_counter}, Paired_Rows {paired_rows},Time {datetime.now()}")
            
            if row_counter > start_row:
                if row_counter % end_row == 0:
                    print("Cleaning Data!")
                    query = "DELETE FROM chat_reply WHERE parent IS NULL"
                    remove_parent_null_table_data(query)
                    break #end inserting and cleaned the data