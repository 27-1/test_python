import os
import pymysql
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/api')
def api():
    return render_template("apiInstance.html")


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