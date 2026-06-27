from flask import Flask, render_template, url_for, request, jsonify, flash, current_app

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registrationForm.html')

if __name__ == '__main__':
    app.run(debug=True)