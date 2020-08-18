from flask import Flask, render_template, url_for, request, jsonify
import data_storage
import datetime

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def login():
    global user_df
    user_df = data_storage.get_data_user()
    return render_template('login.html',error=' ')

@app.route('/index', methods = ['GET','POST'])
def index():
    global username
    username = request.form['username']
    pasw = request.form['pass']
    try:
        role = user_df.loc[(user_df['username']==username) & (user_df['passw']==pasw),'role'].iloc[0]
        if len(user_df[(user_df['username']==username) & (user_df['passw'] == pasw)])>0:
            return render_template('index.html',user = role)
    except:
        return render_template('login.html',error = 'Invalid Creds!')
#    return render_template('index.html',user='all')

@app.route('/update', methods = ['GET','POST'])
def update():
    ordn = request.args.get('ord')
    trans = request.args.get('trans')
    amt = request.args.get('amt')
    next_proc = data_storage.check(ordn,trans)
    if next_proc == 'Not Exist':
        updation = data_storage.update(username,str(datetime.datetime.now().replace(microsecond=0)),ordn,trans,amt)
        return updation
    return next_proc

@app.route('/getdata', methods=['GET','POST'])
def getdata():
    df = data_storage.get_data()
    a = {}
    for i in range(0,len(df)):
        a1 = {"user":df['user'][i],"timestamp":df['timestamp'][i],"order_number":df['order_number'][i],"trans_id":df['trans_id'][i],"Amount":df['Amount'][i]}
        s1 = {"s{}".format(i):a1}
        a.update(s1)
    data = {"data":a}
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7002)
