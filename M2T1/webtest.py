from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/hello')
def hello_again():
    return "<h1>Hello!</h1><p>here's some text</p>"

if __name__ == '__main__':
    app.run(debug=True)