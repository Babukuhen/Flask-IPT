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
    # Get All Employee Details
    data = data_fetch("""SELECT * FROM employee""")
    return make_response(jsonify(data), 200)


@app.route("/employee/<int:id>", methods=["GET"])
def get_employee_by_id(id):
    # Get Employee by Employee ID
    data = data_fetch(f"""SELECT * FROM employee WHERE employee_id = {id}""")
    return make_response(jsonify(data), 200)


@app.route("/employee/<int:id>/department", methods=["GET"])
def get_department_by_employee(id):
    # Gets Department Location by Employee ID
    query = f"""
    SELECT department.department_location
    FROM employee
    INNER JOIN department 
    ON employee.department_id = department.department_id 
    WHERE employee.employee_id = {id}
    """
    data = data_fetch(query)
    if not data:
        return make_response(jsonify({"Message": "Employee not found"}), 404)
    return make_response(jsonify({"Department Location": data[0]["department_location"]}), 200)


@app.route("/employee", methods=["POST"])
def add_employee():
    pass


@app.route("/employee/<int:id>", methods=["PUT"])                       # FIX
def update_employee(id):
    pass


@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    pass


@app.route("/employee/format", methods=["GET"])
def get_params():
    pass



if __name__ == "__main__":
    app.run(debug=True)