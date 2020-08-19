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
    username = request.form['username']
    pasw = request.form['pass']
    try:
        role = user_df.loc[(user_df['username']==username) & (user_df['passw']==pasw),'role'].iloc[0]
        if len(user_df[(user_df['username']==username) & (user_df['passw'] == pasw)])>0:
            return render_template('index.html',user = username, role=role)
    except:
        return render_template('login.html',error = 'Invalid Creds!')
#    return render_template('index.html',user='all')

@app.route('/update', methods = ['GET','POST'])
def update():
    ordn = request.args.get('ord')
    trans = request.args.get('trans')
    amt = request.args.get('amt')
    user = request.args.get('user')
    next_proc = data_storage.check(trans)
    if next_proc == 'Not Exist':
        updation = data_storage.update(user,str(datetime.datetime.now().replace(microsecond=0)),ordn,trans,amt)
        return 'success'
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

@app.route('/newuser', methods = ['GET','POST'])
def newusercreate():
    user = request.args.get('user_name')
    passw = request.args.get('user_password')
    role = request.args.get('user_role')
    create_user = data_storage.create_new_user(user,passw,role)
    return create_user

@app.route('/olduserupdate', methods = ['GET','POST'])
def newuserupdate():
    user = request.args.get('user_name')
    passw = request.args.get('user_password')
    role = request.args.get('user_role')
    create_user = data_storage.update_new_user(user,passw,role)
    return create_user

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7001)
