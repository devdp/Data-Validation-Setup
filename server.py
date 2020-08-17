from flask import Flask, render_template, url_for, request
import data_storage
import datetime

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def login():
    global user_df
    user_df = data_storage.get_data_user()
    return render_template('login.html')

@app.route('/index', methods = ['GET','POST'])
def index():
    global username
    # username = request.form['username']
    # pasw = request.form['pass']
    # if len(df[(user_df['username']==username) & (user_df['passw'] == pasw)])>0:
    #     return render_template('index.html',user = role)
    # else:
    #     return render_template('login.html',error = 'Invalid Creds!')
    return render_template('index.html',user = 'all')

@app.route('/update', methods = ['GET','POST'])
def update():
    ordn = request.args.get('ord')
    trans = request.args.get('trans')
    amt = request.args.get('amt')
    next_proc = data_storage.check(ordn,trans,amt)
    if next_proc == 'Not Exist':
        updation = data_storage.update(username,str(datetime.datetime.now().replace(microsecond=0)),ordn,trans,amt)
        return updation
    return next_proc

if __name__ == '__main__':
    app.run()