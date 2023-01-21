import json
import sqlite3
from datetime import datetime

current_year_month = "2023-01"

sql_transaction = []

connection = sqlite3.connect(f'{current_year_month}.db')
c = connection.cursor()

#file path of the dataset
file_path = ""

def create_table():
    c.execute(
      """
        CREATE TABLE IF NOT EXISTS chat_reply(
            parent_id TEXT PRIMARY KEY,
            comment_id TEXT UNIQUE,
            parent TEXT,
            comment TEXT,
            subreddit TEXT
            unix INT,
            score INT
        )
      """
    )
    

if __name__ == "__main__":
    # This will create a sql lite table.
    create_table()
    row_counter = 0
    paired_rows = 0
    
    # with open(file_path)
    

