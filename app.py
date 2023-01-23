import tensorflow as tf
from model.chatbot_database import create_table,find_parent,find_existing_score,\
    sql_insert_replace_comment,sql_insert_has_parent,sql_insert_no_parent
from datetime import datetime
import json


#file path of the dataset
file_path = "Dataset/RC_2015-01"


def format_data(data):
    # This will format the data contain (\n,\r,single quote - double quote)
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data

def acceptable_data(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True
    
# def singleInsert():
#     c.execute("""INSERT INTO chat_reply SET(t3_2qx5au,t1_cnaudqw,lorlipone,KotakuInAction,1420075348,2)""")


if __name__ == "__main__":
    # This will create a sql lite table.
    create_table()
    row_counter = 0
    paired_rows = 0
    
    # Here this will open the file and extract the data.
    with open(file_path,buffering=2000) as f:
        for row in f:
            # print(row)
            # if row_counter >= 5:
            #     break
            # row_counter += 1
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']
            comment_id = row['name']
            author = row['author']
            parent_data = find_parent(parent_id)
            if score >= 2:
                if acceptable_data(body):
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            sql_insert_replace_comment(parent_id=parent_id,comment_id=comment_id,
                                                       author=author,parent_data=parent_data,subreddit=subreddit,
                                                       created_utc=created_utc,score=score)
                    else:
                        if parent_data:
                            sql_insert_has_parent(parent_id=parent_id,comment_id=comment_id,
                                                author=author,parent=parent_data,subreddit=subreddit,
                                                created_utc=created_utc,score=score)
                            paired_rows += 1
                        else:
                            # even though it doesn't have the parent passing the parent_id as false to avoid query error.
                            sql_insert_no_parent(parent_id=parent_id,comment_id=comment_id,
                                                author=author,subreddit=subreddit,
                                                created_utc=created_utc,score=score)
                            
            if row_counter == 100000:
                print(f"Row Counter Value {row_counter}, Paired_Rows {paired_rows},Time {datetime.now()}")
            if row_counter == 500000:
                print(f"Row Counter Value {row_counter}, Paired_Rows {paired_rows},Time {datetime.now()}")
            if row_counter == 1000000:
                print(f"Row Counter Value {row_counter}, Paired_Rows {paired_rows},Time {datetime.now()}")
                break