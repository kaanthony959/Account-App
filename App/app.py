import sqlite3
import logging
from flask import Flask, render_template,url_for,redirect,request

app = Flask(__name__)

def connectDB():
    try:
        conn =sqlite3.connect(r'D:/Account App/Database/account_app.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                       username NOT NULL UNIQUE,
                       password NOT NULL)''')
        conn.commit()
        conn.close
    except Exception as e:
        logging.critical(f'Error when connect to DB:{e}') 

def ExecuteSQLQuery(sql_Query, params, fetch_result=False):
    try:
        return_id = -1
        conn =sqlite3.connect(r'D:/Account App/Database/account_app.db')
        cursor = conn.cursor()
        last_rowid = cursor.lastrowid
        cursor.execute(sql_Query, params)
        if fetch_result:
            results = cursor.fetchall()
            return_results = results
        else:
            results = cursor.lastrowid
            if results == last_rowid:
                return_id = 0
            return_id = 1
        conn.commit()
        conn.close
        if return_id > -1:
            return return_id
        return return_results

    except Exception as e:
        errorMsg = str(e)
        logging.exception('Error when running sql:')
        logging.debug(f'Error when running sql: {sql_Query},{params}')

@app.route("/")
def index(): 
    return render_template('index.html')

@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        if request.values['send'] == '送出':
            registerResult = Register_back(request.values['username'], request.values['password'])
            if registerResult:
                return render_template('register.html', result="True")
            return render_template('register.html', alert='此帳號已有人註冊', result="False")
    return render_template('register.html', result="")

def Initialize():
    logging.basicConfig(level = logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s', 
                        filename=r'D:/Account App/Logs/app.log', 
                        filemode = 'w')
    connectDB()
    logging.debug('Application Initialized')

def Register_back(username, password):
    checkUserExistQuery = 'SELECT * FROM Users where username = ?'
    params = (username,)
    checkUserExist = ExecuteSQLQuery(checkUserExistQuery, params, True)
    if len(checkUserExist) > 0:
        return False
    sqlQuery = 'INSERT INTO Users (username, password) VALUES(?, ?)'
    params = (username, password)
    if ExecuteSQLQuery(sqlQuery, params):
        return True
    return False

def main():
    Initialize()
    app.run(debug=True)

if __name__ == '__main__':
    main()