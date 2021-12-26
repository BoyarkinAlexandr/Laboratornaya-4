from flask import Flask, render_template, request, redirect
import psycopg2

app=Flask(__name__)

conn = psycopg2.connect(database="service",
                        user="alexandrboyarkin",
                        password="1234",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')  # запрос к данным формы
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password),))
            records = list(cursor.fetchall())
            if len(password) and len(username) == 0:
                return render_template('error.both.html')
            elif len(username) == 0:
                return render_template('error.name.html')
            elif len(password) == 0:
                return render_template('error.pass.html')

            return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def reg():
    if request.method == 'POST':
        name = request.form.get('name')
        login1 = request.form.get('login')
        password = request.form.get('password')

        cursor.execute("Select * FROM service.users WHERE login=%s", (str(login1),))
        records = list(cursor.fetchall())
        if len(name) == 0:
            return render_template('reg.error.html')
        elif len(login1) == 0:
            return render_template('reg.error.html')
        elif len(password) == 0:
            return render_template('reg.error.html')
        else:
            if len(records) != 0:
                return render_template('123.html')
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login1), str(password)))
                conn.commit()

                return redirect('/login/')


    return render_template('registration.html')