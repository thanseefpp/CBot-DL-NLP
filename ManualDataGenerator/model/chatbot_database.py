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
            comment CHAR,
            subreddit CHAR,
            unix INT,
            score INT
        );
      """
    )

def find_parent(id):
    try:
        sql = "SELECT comment FROM chat_reply WHERE comment_id = '{}' LIMIT 1".format(id)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
    except Exception as e:
        return False

def find_existing_score(id):
    try:
        sql = "SELECT score FROM chat_reply WHERE parent_id = '{}' LIMIT 1".format(id)
        c.execute(sql)
        result = c.fetchone()
        if result != None:
            return result[0]
        else: return False
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
            except:
                pass
        connection.commit()
        sql_transaction = []
        
def remove_parent_null_table_data(query):
    try:
        c.execute(query)
        connection.commit()
        c.execute("VACUUM")
        connection.commit()
    except Exception as e:
        return False
    
def sql_insert_replace_comment(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """UPDATE chat_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?, subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(parentid, commentid, parent, comment, subreddit, int(time), score, parentid)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_has_parent(commentid,parentid,parent,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO chat_reply (parent_id, comment_id, parent, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}","{}",{},{});""".format(parentid, commentid, parent, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))

def sql_insert_no_parent(commentid,parentid,comment,subreddit,time,score):
    try:
        sql = """INSERT INTO chat_reply (parent_id, comment_id, comment, subreddit, unix, score) VALUES ("{}","{}","{}","{}",{},{});""".format(parentid, commentid, comment, subreddit, int(time), score)
        transaction_bldr(sql)
    except Exception as e:
        print('s0 insertion',str(e))