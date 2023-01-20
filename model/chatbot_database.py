import json
import sqlite3
from datetime import datetime

current_year_month = "2023-01"

sql_transaction = []

connection = sqlite3.connect(f'{current_year_month}.db')
c = connection.cursor()


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
    

