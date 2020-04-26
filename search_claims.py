import os
import sqlite3 
from tqdm import tqdm
from nltk import tokenize

db_file = "cord19_2020-04-26.db"
conn = sqlite3.connect(db_file)
c = conn.cursor()

signalwords_list = ["show that"," conclude that", "believe that"] # "because -of"

writer = open("claims.txt",'w',encoding='utf-8')
for signal in signalwords_list:
    c.execute(
        "SELECT text FROM body_text WHERE text LIKE '%"+ signal +"%'"
    )
    rows = c.fetchall()
    print(signal, file=writer)
    for row in rows:
        #print(row)
        for sent in tokenize.sent_tokenize(row[0]):
            if signal in sent:
                writer.write(sent+'\n')
    break