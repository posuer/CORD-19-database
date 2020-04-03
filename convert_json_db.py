import os
import sqlite3 
import urllib.request
import json

url = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/2020-03-27/"

subsets = {
    "comm_use_subset": "comm_use_subset.tar.gz",
    "noncomm_use_subset": "noncomm_use_subset.tar.gz",
    "custom_license": "custom_license.tar.gz",
    "biorxiv_medrxiv": "biorxiv_medrxiv.tar.gz",
}

for sub_type, file_name in subsets.items():
    if os.path.exists(file_name):
        continue
    print('Downloading ', file_name)
    urllib.request.urlretrieve(url+file_name, file_name)

for sub_type, file_name in subsets.items():
    if os.path.exists(sub_type):
        continue
    print('Unziping ', file_name)
    #os.system("gunzip "+file_name)
    os.system("tar -zxf "+file_name)

db_file = "cord19.db"
conn = sqlite3.connect(db_file)
c = conn.cursor()

for sub_type, file_name in subsets.items():
    for filename in os.listdir(sub_type):
        if filename.endswith(".json"):
            print("Inserting ", filename)
            f = open(os.path.join(sub_type,filename),'r',encoding='utf-8')

            contents = json.loads(f.read())
            paper_id = contents["paper_id"]
            title = contents["metadata"]["title"]
            abstract = contents["abstract"][0]["text"]
  
            c.execute(
                    "INSERT INTO papers(paper_id, title, abstract, subset_type) VALUES (?, ?, ?, ?)",
                    (paper_id, title, abstract, sub_type)
                )
            paragraph_id = 0
            for paragraph in contents["body_text"]:
                text = paragraph["text"]
                section = paragraph["section"]
                c.execute(
                    "INSERT INTO body_text(paper_id, paragraph_id, section, text) VALUES (?, ?, ?, ?)",
                    (paper_id, paragraph_id, section, text)
                )
                paragraph_id += 1
            conn.commit()
            f.close()
       
conn.close()
