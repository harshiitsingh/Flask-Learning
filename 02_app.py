# INTEGRATING HTML WITH FLASK WEB FRAMEWORK WITH HTTP VERBS (GET AND POST)
# It is also called JINJA2 template technique
# JINJA 2 means if you have different code/data it will help you to integrate with flask or webpage.

from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('submit.html')

@app.route('/success/<int:score>')
def success(score):
    res = ""
    if score>=30:
        res = "PASS"
    else:
        res = "FAIL"
    return render_template('result.html', result = res) # jinja 2 template engine is helping here, integrating flask with html

@app.route('/fail/<int:score>')
def fail(score):
    return 'The person has failed and the marks is ' + str(score)

## Result checker html page
@app.route('/submit', methods= ['POST', 'GET'])
def submit():
    total_score = 0
    if request.method == 'POST':
        science = float(request.form['science']) # by default it will be in the form of string, so convert it into the float.
        maths = float(request.form['maths']) # should match with the name input in html file.
        c = float(request.form['c'])
        data_science = float(request.form['datascience'])
        total_score = (science+maths+c+data_science)/4
    
    res = ""
    # if total_score>=50:
    #     res = "success"
    # else: res = "fail"        
    # return redirect(url_for(res, score=total_score))
    return redirect(url_for('success', score=total_score))


if __name__ == "__main__":
    app.run(debug=True)