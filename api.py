from flask import Flask, make_response, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "676jvllavan"
app.config["MYSQL_DB"] = "emp_dep_db"

app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)


@app.route("/")
def page_display():
    return "<p>Hello, World!</p>"


def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    cur.close()
    return data


@app.route("/employee", methods=["GET"])
def get_employee():
    data = data_fetch("""SELECT * FROM employee""")
    return make_response(jsonify(data), 200)


if __name__ == "__main__":
    app.run(debug=True)