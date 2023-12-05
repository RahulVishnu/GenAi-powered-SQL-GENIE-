# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import os

import sqlite3
import pandas as pd
from langchain import OpenAI, SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from secret import api_key

df = pd.read_csv('CC.csv')

conn = sqlite3.connect('CC_tot.sqlite')

# +
cur = conn.cursor()

table_name = 'CC_tot'
query = fquery = f"""CREATE TABLE IF NOT EXISTS {table_name} (Date received Date, Product Text, "Sub-product" Text, Issue Text, "Sub-issue" Text,
       Consumer Complaint Text, "Company Public Response" Text, Company Text,
       State Text, ZIP code Text, Tags Text,  "Consumer consent provided?" Text,
       Submitted via Text, "Date Sent to Company" Date,
       "Company Response to Consumer" Text, "Timely response?" Text,
       "Consumer disputed?" Text, Complaint ID Number )"""
cur.execute(query)
# -

df.to_sql(table_name, conn, if_exists='replace', index = False)
conn.commit()

# +
# # !ls | grep cc.sqlite
# -

def read_query(sql):
    conn = sqlite3.connect('CC_tot.sqlite')
    cur = conn.cursor()
    res_list = []
    data = cur.execute(sql)
    rows = cur.fetchall()
    names = list(map(lambda x: x[0], data.description))
    res_list.append(names)
    for row in rows:
        res_list.append(list(row))
    conn.close()
    
    res = pd.DataFrame(res_list[1:], columns=res_list[0])
    return res


def output_res(question):
    
    db = SQLDatabase.from_uri('sqlite:///CC_tot.sqlite')

    os.environ['OPENAI_API_KEY'] = api_key
    llm = OpenAI(temperature = 0)

    db_chain = SQLDatabaseChain(llm = llm, database = db, verbose = True, use_query_checker=True,
        return_intermediate_steps=True,)

    response = db_chain(question)
    print(response)

    prompt = response["intermediate_steps"][1]
    answer = read_query(prompt)
    
    return answer, prompt
# read_query('SELECT "Consumer Complaint" FROM cc WHERE "Company" = "M&T BANK CORPORATION" AND "Date received" > "01-01-2014" LIMIT 5;')






