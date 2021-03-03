from flask import Flask, render_template, jsonify, request, redirect
import argparse
import requests
import pymysql.cursors
from datetime import datetime

app = Flask(__name__, template_folder='.')
app.debug = True
arguments = None


def get_db_connection():
    return pymysql.connect(host='192.168.1.5',
                           user='flask',
                           password='assword',
                           database='mydb',
                           cursorclass=pymysql.cursors.DictCursor)


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nvr-token", help="NVR api token", default='79be20cd54214a30bf2ef8347915c084')
    parser.add_argument("-p", "--port", help="Server port", default=80)
    parser.add_argument("--ssl-key", help="Path to ssl key")
    parser.add_argument("--ssl-cert", help="Path to ssl certificate")
    return parser.parse_args()


@app.route("/control")
def control():
    headers = {"key": arguments.nvr_token}
    response = requests.get('https://nvr.miem.hse.ru/api/sources/',
                            headers=headers)
    cams = response.json()
    cams.append({'id': 'test','name': 'test'})
    return render_template("control.html", cams=cams)

@app.route("/photo")
def photo():
    return render_template('photo.html')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/vmix")
def vmix():
    return render_template('vmix.html')

@app.route("/vmix_about")
def vmix_about():
    return render_template('vmix_about.html')

@app.route("/timesheet")
def timesheet():
    return render_template('timesheet.html')

@app.route("/hw7")
def hw7():
    with get_db_connection() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM teacher"
            cursor.execute(sql)
            teachers = cursor.fetchall()
            sql = "SELECT * FROM auditory"
            cursor.execute(sql)
            auditories = cursor.fetchall()
    return render_template('hw7.html', teachers=teachers, auditories=auditories)

@app.route("/atata")
def atata():
    return render_template('atata.html')

@app.route("/graph")
def graph():
    if request.method == 'GET':
        result = []
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                for lesson_num in range(1, 9):
                    sql = f"SELECT * FROM lesson where number = {lesson_num} and date = '{datetime.today().strftime('%Y-%m-%d')}'"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    result.append([str(8+lesson_num)+':00', len(data)])
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200

@app.route("/pie")
def pie():
    if request.method == 'GET':
        result = []
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM teacher"
                cursor.execute(sql)
                teachers = cursor.fetchall()
                for teacher in teachers:
                    sql = f"SELECT * FROM lesson where teacher = {teacher['id']} and date = '{datetime.today().strftime('%Y-%m-%d')}'"
                    cursor.execute(sql)
                    data = cursor.fetchall()
                    result.append([teacher['name'], len(data)])
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200

@app.route("/table")
def table():
    if request.method == 'GET':
        result = []
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM auditory"
                cursor.execute(sql)
                auds = cursor.fetchall()
                for aud in auds:
                    result.append([aud['id'], aud['capacity'], get_quality(aud)])
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200

@app.route("/knapsack", methods=['GET', 'POST'])
def knapsack():
    if request.method == 'GET':
        data = []
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"SELECT * FROM auditory"
                cursor.execute(sql)
                auds = cursor.fetchall()
                for aud in auds:
                    data.append((aud['id'], get_quality(aud), aud['capacity']))
                result = knapSack(int(request.args.get('max_cap', 0)), data, len(data))
                ans = []
                for i in result:
                    ans.append(i[0])
        return jsonify(isError=False, message="Success", statusCode=200, data=ans), 200

@app.route("/auditory", methods=['GET', 'POST'])
def auditory():
    if request.method == 'GET':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM auditory"
                cursor.execute(sql)
                result = cursor.fetchall()
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200
    if request.method == 'POST':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"insert into auditory values ({request.form.get('auditory')}, " \
                      f"{request.form.get('capacity')}, {int(bool(request.form.get('microphone')))}, " \
                      f"{int(bool(request.form.get('projector')))}, {int(bool(request.form.get('board')))}, " \
                      f"{int(bool(request.form.get('computer')))});"
                cursor.execute(sql)
            connection.commit()
        return redirect('hw7')

@app.route("/teacher", methods=['GET', 'POST'])
def teacher():
    if request.method == 'GET':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM teacher;"
                cursor.execute(sql)
                result = cursor.fetchall()
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200
    if request.method == 'POST':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"insert into teacher (name) values ('{request.form.get('name')}');"
                cursor.execute(sql)
            connection.commit()
        return redirect('hw7')

@app.route("/lesson", methods=['GET', 'POST'])
def lesson():
    if request.method == 'GET':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM lesson"
                cursor.execute(sql)
                result = cursor.fetchall()
        return jsonify(isError=False, message="Success", statusCode=200, data=result), 200
    if request.method == 'POST':
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                sql = f"insert into lesson values ({request.form.get('auditory')}, {request.form.get('teacher')}, " \
                      f" '{request.form.get('date')}', {request.form.get('number')});"
                cursor.execute(sql)
            connection.commit()
        return redirect('hw7')

def create_tables():
    with get_db_connection().cursor() as cursor:
        sql = [
            """
            CREATE TABLE IF NOT EXISTS auditory (
                id int unsigned primary key AUTO_INCREMENT,
                capacity int unsigned not null,
                microphone boolean default 0, 
                projector boolean default 0, 
                board boolean default 0, 
                computer boolean default 0);
            """,
            """
            CREATE TABLE IF NOT EXISTS teacher (
                id int unsigned primary key AUTO_INCREMENT, 
                name varchar(120) NOT NULL);
            """,
            """
            CREATE TABLE IF NOT EXISTS lesson (
                auditory int unsigned,
                teacher int unsigned,
                date DATE not null,
                number int unsigned not null,
                FOREIGN KEY(teacher) REFERENCES teacher(id),
                FOREIGN KEY(auditory) REFERENCES auditory(id));
            """
        ]
        for s in sql:
            cursor.execute(s)

def get_quality(record):
    return int(record['microphone'])*15 + int(record['projector'])*20 + \
           int(record['board'])*5 + int(record['computer'])*10

def knapSack(students, data, n):
    '''
    0 - aud
    1 - qual
    2 - cap
    '''
    if n == 0 or students == 0:
        return []
    if (data[n-1][2] > students):
        return knapSack(students, data, n-1)
    else:
        next_knapsack = knapSack(students - data[n-1][2], data, n-1)
        if data[n-1][1] + sum(i[1] for i in next_knapsack) > sum(i[1] for i in next_knapsack):
            return [data[n-1], *next_knapsack]
        else:
            return knapSack(students, data, n-1)

if __name__ == "__main__":
    arguments = get_arguments()
    create_tables()
    # ssl_context = (arguments.ssl_cert, arguments.ssl_key)
    app.run(host='0.0.0.0', port=arguments.port)  # , ssl_context=ssl_context)