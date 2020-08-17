from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://eukrnjwvnp:xmGYDFGk67@localhost/eukrnjwvnp?host=localhost?data=3306")
engine2 = create_engine("mysql+pymysql://eukrnjwvnp:xmGYDFGk67@localhost/eukrnjwvnp?host=localhost?users=3306")
def updatenew(user, timestamp, order_number, trans_id, Amount):
    query = "insert into data values("+str(user)+",'"+timestamp+"','"+order_number+"','"+trans_id+"','"+Amount+"');"
    with engine.begin() as conn:
        conn.execute(query)
    return 'updated'

def get_data_users():
    query = "select * from users;"
    return pd.read_sql(query,engine2)

def get_data():
    query = "select * from data order by timestamp desc;"
    return pd.read_sql(query,engine)

def check(ordn,trans,amt):
    query = "select * from data;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df["order_number"] == ordn) & (df['trans_id'] == trans) & (df['Amount'] == amt))[0])
    if len(index_num)>0:
        index_num = int(index_num[0])+1
        return 'Already Exist At Row Number {}'.format(str(index_num))
    else:
        return 'Not Exist'
    return 'Not able to check'