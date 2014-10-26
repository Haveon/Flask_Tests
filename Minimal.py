from flask import Flask

#First argument: name of the app's module of package
app = Flask(__name__)

#Decorate hello world with route
#Route specifies the url route
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    app.run()