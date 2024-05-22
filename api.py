from flask import Flask, make_response, jsonify, request
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
    # Adds Employee to the Database
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    department_id = info["department_id"]

    cur.execute("""INSERT INTO employee (first_name, last_name, department_id) VALUE (%s, %s, %s)""",
        (first_name, last_name, department_id))
    mysql.connection.commit()
    
    print(f"Row(s) Affected :{cur.rowcount}")
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": "Employee Added Successfully", "Rows Affected": rows_affected}), 201)


@app.route("/employee/<int:id>", methods=["PUT"])
def update_employee(id):
    # Updates Employee from the Database
    cur = mysql.connection.cursor()
    info = request.get_json()
    first_name = info["first_name"]
    last_name = info["last_name"]
    department_id = info["department_id"]

    cur.execute("""UPDATE employee SET first_name = %s, last_name = %s, department_id = %s WHERE employee_id = %s """,
        (first_name, last_name, department_id, id))
    mysql.connection.commit()

    print(f"Row(s) Affected :{cur.rowcount}")
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": f"Employee '{id}' Updated Successfully", "Rows Affected": rows_affected}), 200,)


@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    # Deletes Employee from the Database
    cur = mysql.connection.cursor()
    cur.execute(f"""DELETE FROM employee where employee_id = {id}""")
    mysql.connection.commit()

    print(f"Row(s) Affected :{cur.rowcount}")
    rows_affected = cur.rowcount
    cur.close()
    return make_response(jsonify({"Message": f"Employee '{id}' Deleted Successfully", "Rows Affected": rows_affected}), 200)


@app.route("/employee/format", methods=["GET"])
def get_params():
    fmt = request.args.get('id')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format":fmt, "foo":foo}),200)


if __name__ == "__main__":
    app.run(debug=True)