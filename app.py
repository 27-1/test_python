import os
import pymysql
from flask import Flask, render_template, Response, request
import requests
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api', methods=['POST'])
def api():
    url = request.form["url"]
    payload = request.form["payload"]
    headers = request.form["headers"]
    method = request.form["method"]
    if method.upper == "GET":
        r = requests.get(url, params=payload, headers=headers)
        return Response(json.dumps(r), mimetype='application/json')
    elif method.upper == "POST":
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        return Response(json.dumps(r), mimetype='application/json')
    elif method.upper == "PUT":
        r = requests.put(url, data=json.dumps(payload), headers=headers)
        return Response(json.dumps(r), mimetype='application/json')
    elif method.upper == "DELETE":
        r = requests.delete(url, data=json.dumps(payload), headers=headers)
        return Response(json.dumps(r), mimetype='application/json')


@app.route('/mysql')
def mysql():
    MYSQL_HOST = os.environ("MYSQL_HOST", None)
    MYSQL_USER = os.environ("MYSQL_USER", None)
    MYSQL_PASS = os.environ("MYSQL_PASS", None)
    DB_NAME = os.environ("DB_NAME", None)
    if not MYSQL_HOST or not MYSQL_USER or not MYSQL_PASS or not DB_NAME:
        return Response("参数不全")

    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASS, db=DB_NAME, charset='utf8')
    cur = conn.cursor()
    sql = "show tables;"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return Response(u)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)