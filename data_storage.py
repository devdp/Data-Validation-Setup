from sqlalchemy import create_engine
import pandas as pd
import numpy as np

engine = create_engine("mysql+pymysql://root:passowrd@IP/db?host=host")

def update(user, timestamp, order_number, trans_id, Amount):
    query = "insert into data values('"+str(user)+"','"+timestamp+"','"+order_number+"','"+trans_id+"','"+Amount+"');"
    with engine.begin() as conn:
        conn.execute(query)
    return 'updated'

def get_data_user():
    query = "select * from users;"
    return pd.read_sql(query,engine)

def get_data():
    query = "select * from data order by timestamp desc;"
    return pd.read_sql(query,engine)

def check(trans):
    query = "select * from data;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df["trans_id"] ==trans))[0])
    if len(index_num)>0:
        index_num = int(index_num[0])
        ordis = df['order_number'][index_num]
        return 'Already Exist Order Number : {}'.format(str(ordis))
    else:
        return 'Not Exist'
    return 'Not able to check'

def create_new_user(user,passw,role):
    query = "select * from users;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df['username']==user))[0])
    if len(index_num)>0:
        return 'User Already Exists'
    else:
        query = "insert into users values('"+user+"','"+passw+"','"+role+"');"
        with engine.begin() as conn:
            conn.execute(query)
        return 'New User Added'

def update_new_user(user,passw,role):
    query = "select * from users;"
    df = pd.read_sql(query,engine)
    index_num = list(np.where((df['username']==user))[0])
    if len(index_num)>0:
        query = "UPDATE users SET passw = '"+passw+"', role = '"+role+"' where username = '"+user+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return 'Successfully Updated User'    
    else:
        return 'User Does Not Exist'

def uprec(amtup,orderup,transup,userr):
    df = pd.read_sql("select * from data;",engine)
    if(len(df.loc[df['trans_id']==transup])):
        query = "UPDATE data SET user='"+userr+"', order_number='"+orderup+"', Amount='"+amtup+"' where trans_id='"+transup+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Updated Record"
    else:
        return "Record Doesn't Exist"

def delrec(trid):
    df = pd.read_sql("select * from data;",engine)
    if(len(df.loc[df['trans_id']==trid])):
        query = "Delete from data where trans_id='"+trid+"';"
        with engine.begin() as conn:
            conn.execute(query)
        return "Successfully Deleted Record"
    else:
        return "Record Doesn't Exist"
