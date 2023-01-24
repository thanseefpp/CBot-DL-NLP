import sqlite3
import pandas as pd

current_year_month = "2023-01"

connection = sqlite3.connect(f'{current_year_month}.db')
c = connection.cursor()
limit = 10000 # you can change the limit to store more data.
last_unix = 0
current_length = limit
counter = 0
test_done = False

while current_length == limit:
    dataframe = pd.read_sql(f"SELECT * FROM chat_reply WHERE unix > {last_unix} AND parent NOT NULL AND score > 0 ORDER BY unix ASC LIMIT {limit}",connection)
    last_unix = dataframe.tail(1)['unix'].values[0]
    current_length = len(dataframe)
    if not test_done:
        # Store the parent data to test.from file
        with open('train_test_set/test.from','a', encoding='utf8') as f:
            for content in dataframe['parent'].values:
                f.write(content+'\n')
        # Store the comment data to test.to file
        with open('train_test_set/test.to','a', encoding='utf8') as f:
            for content in dataframe['comment'].values:
                f.write(str(content)+'\n')
        test_done = True
    else:
        # Store the parent data to train.from file
        with open('train_test_set/train.from','a', encoding='utf8') as f:
            for content in dataframe['parent'].values:
                f.write(content+'\n')
        # Store the comment data to train.to file
        with open('train_test_set/train.to','a', encoding='utf8') as f:
            for content in dataframe['comment'].values:
                f.write(str(content)+'\n')
    counter += 1
    if counter % 20 == 0:
        print(counter*limit,'number of rows Completed')
    
    