import sqlite3

current_year_month = "2023-01"

sql_transaction = []

connection = sqlite3.connect(f'{current_year_month}.db')
c = connection.cursor()

def create_table():
    c.execute(
      """
        CREATE TABLE IF NOT EXISTS chat_reply(
            parent_id CHAR PRIMARY KEY,
            comment_id CHAR UNIQUE,
            parent CHAR,
            author CHAR,
            subreddit CHAR,
            created_utc INT,
            score INT
        );
      """
    )
  
def find_parent(id):
    try:
        query = f"""SELECT parent FROM chat_reply WHERE parent_id = {id} LIMIT 1"""
        c.execute(query)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        return False

def find_existing_score(id):
    try:
        query = f"SELECT score FROM chat_reply WHERE parent_id = {id} LIMIT 1"
        c.execute(query)
        result = c.fetchone()
        if result != None:
            return result[0]
        else:
            return False
    except Exception as e:
        return False
    
def transaction_bldr(query):
    global sql_transaction
    sql_transaction.append(query)
    if len(sql_transaction) > 1000:
        c.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                c.execute(s)
                # print(s)
            except:
                pass
        connection.commit()
        sql_transaction = []
    
def sql_insert_replace_comment(parent_id,comment_id,author,parent_data,subreddit,created_utc,score):
    try:
        query = f"""UPDATE chat_reply SET parent_id = {parent_id}, comment_id = {comment_id}, parent = {parent_data}, author = {author}, subreddit = {subreddit}, created_utc = {created_utc}, score = {score}"""
        transaction_bldr(query)
    except Exception as e:
        print("query update error",e)

def sql_insert_has_parent(parent_id,comment_id,parent,author,subreddit,created_utc,score):
    try:
        query = f'''INSERT INTO chat_reply(parent_id, comment_id, parent, author, subreddit, created_utc, score) VALUES ("{parent_id}","{comment_id}","{parent}","{author}","{subreddit}",{created_utc},{score});'''
        transaction_bldr(query)
        print(query)
    except Exception as e:
        print("query parent error",e)

def sql_insert_no_parent(parent_id,comment_id,author,subreddit,created_utc,score):
    try:
        query = f'''INSERT INTO chat_reply(parent_id, comment_id, author, subreddit, created_utc, score) VALUES ("{parent_id}","{comment_id}","{author}","{subreddit}",{created_utc},{score});'''
        transaction_bldr(query)
    except Exception as e:
        print("query no parent error",e)