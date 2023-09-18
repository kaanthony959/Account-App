from flask import Flask, render_template,url_for,redirect,request

app = Flask(__name__)

@app.route("/")
def index(): 
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/second')
def second():
    return redirect(url_for('index'))

@app.route("/Flask")
def flask():
    return "Hello Flask!"

@app.route('/request_test', methods=['POST','GET'])
def request_test():
    if request.method == 'POST':
        if request.values['send'] == '送出':
            return render_template('request_test.html', name=request.values['user'])
    return render_template('request_test.html',name="")

if __name__ == "__main__":
    app.run(debug=True)