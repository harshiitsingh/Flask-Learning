from flask import Flask, redirect, url_for

## WSGI APPLICATION
# creating the object of the flask app.
app = Flask(__name__) # creating the app name and initializing it through the flask. Providing one parameter
# This object is the WSGI application which will be interacting (a standard) with the server and web application.

@app.route('/') # creating a decorator
def welcome():
    return "Welcome! I am Harshit Singh"

@app.route('/members') # binding function should be different.
def members(): # don't make the name of functions same.
    return "Welcome! I am Harshit Singh from CSE"

## Let's Create the URL Dynamically or URL BUILDING
## BUILDING URL DYNAMICALLY
## VARIABLE RULES AND URL BUILDING
@app.route('/success/<int:score>')
def success(score):
    return 'The person has passed and the marks is ' + str(score)

@app.route('/fail/<int:score>')
def fail(score):
    return 'The person has failed and the marks is ' + str(score)

## RESULT CHECKER
@app.route('/results/<int:marks>')
def results(marks):
    result = ""
    if marks<30: result= "fail"
    else: result= "success"
    # return result
    return redirect(url_for(result, score=marks))

if __name__ == "__main__":
    app.run(debug=True) # debug = True means when we'll open the web app and made some update in the code then we don't need to run the code again and again, just refresh the page.
