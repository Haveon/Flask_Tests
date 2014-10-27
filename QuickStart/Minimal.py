from flask import Flask

#First argument: name of the app's module of package
app = Flask(__name__)

@app.route('/')
def index():
    return "Index Page"

#Decorate hello world with route
#Route specifies the url route
@app.route('/hello')
def hello_world():
    return 'Hello World'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' %username

@app.route('/add/<float:num1>/<float:num2>')
def addition(num1,num2):
    #needs to return a str to print on page
    return str(num1+num2)


if __name__ == '__main__':
    app.run(debug=False)