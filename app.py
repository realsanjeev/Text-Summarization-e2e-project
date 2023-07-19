from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', method=['GET', 'POST'])
def home():
    return '<h1>working!</h1>'

if __name__=="__main__":
    app.run(debug=True)