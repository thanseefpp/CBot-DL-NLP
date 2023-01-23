import sqlite3

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
            subreddit TEXT,
            unix INT,
            score INT
        )
      """
    )
  
def find_parent(id):
    try:
        query = f"SELECT comment FROM chat_reply WHERE comment_id = {id} LIMIT 1"
        c.execute(query)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        return False