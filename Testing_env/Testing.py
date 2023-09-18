import sqlite3
import logging

def connectDB():
    try:
        conn =sqlite3.connect(r'D:/Account App/Database/account_app_test.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS Users (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                       username NOT NULL UNIQUE,
                       password NOT NULL''')
        conn.commit()
        conn.close
    except Exception as e:
        logging.critical(f'Error when connect to DB: {e}')

def ExecuteSQLQuery(sql_Query, params, fetch_result=False):
    try:
        return_id = -1
        conn =sqlite3.connect(r'D:/Account App/Database/account_app_test.db')
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

def Initialize():
    logging.basicConfig(level = logging.DEBUG, format = '%(ascttime)s - %(levelname)s - %(message)s', 
                        filename=r'D:/Account App/Testing_env/app.log', 
                        filemode = 'w')

def LoginSimulate():
    print('1. Register')
    print('2. Login')
    print('3. Exit')
    userinput = input('Please input the number')
    if userinput == '1':
        Register()
    elif userinput == '2':
        Login()


def Register():
    username = input('Please input username')
    password = input('Please input password')
    checkUserExistQuery = 'SELECT * FROM Users where username = ?'
    params = (username,)
    checkUserExist = ExecuteSQLQuery(checkUserExistQuery, params)
    if len(checkUserExist) > 0:
        print('The username already registed')
    sqlQuery = 'INSERT INTO Users (username, password) VALUES(?, ?)'
    params = (username, password)
    if ExecuteSQLQuery(sqlQuery, params):
        print("register successful")

def Login():
    username = input('Please input username')
    password = input('Please input password')
    sqlQuery = "SELECT * FROM Users where username = ? and password = ?"
    params = (username, password)
    sqlResult = ExecuteSQLQuery(sqlQuery, params, True)
    if len(sqlResult) <= 0 :
        print('login fail')
    else:
        print('login successful')

def main():
    Initialize()
    LoginSimulate()

if __name__ == "__main__":
    main()