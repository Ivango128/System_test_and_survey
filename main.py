from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create-test')
def create_test():
    return render_template('create-test.html')

if __name__ == '__main__':
    app.run(debug=True)