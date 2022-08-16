import imp
from pickle import NONE
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/connect', methods=['GET', 'POST'])
def connect():
    # render_template('connect.html')
    

    return render_template('connect.html')
    # return redirect(url_for('submit', name=name))

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method=='POST':
        password = request.form.to_dict()
        name = password.get('name', NONE)
        # email = request.form.get('email')
        # phone = request.form('phone')
        # address = request.form('address')
        # return redirect(url_for('submit', name=name))
        print(password)
        return render_template('submit.html', name=name)
        
    

if __name__=="__main__":
    app.run(debug=True)