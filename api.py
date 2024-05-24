from flask import Flask, make_response, jsonify, request, Response
from flask_mysqldb import MySQL
import dicttoxml
from xml.dom.minidom import parseString

app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "676jvllavan"       # Enter Your Password
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


def format_response(data, format):
    if format == "xml":
        xml = dicttoxml.dicttoxml(data, custom_root='response', attr_type=False)
        dom = parseString(xml)
        xml_str = dom.toprettyxml()
        return Response(xml_str, mimetype='application/xml')
    else:
        return make_response(jsonify(data), 200)


@app.route("/employee", methods=["GET"])
def get_employee():
    # Get All Employee Details
    data = data_fetch("""SELECT * FROM employee""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)


@app.route("/employee/<int:id>", methods=["GET"])
def get_employee_by_id(id):
    # Get Employee by Employee ID
    data = data_fetch(f"""SELECT * FROM employee WHERE employee_id = {id}""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)


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
    response_format = request.args.get('format', 'json')
    if not data:
        return make_response(jsonify({"message": "Employee not found"}), 404)
    return format_response({"Department Location": data[0]["department_location"]}, response_format)


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
    
    rows_affected = cur.rowcount
    cur.close()
    
    response_format = request.args.get('format', 'json')
    response_data = {"message": "Employee Added Successfully", "rows_affected": f"Rows Affected: {rows_affected}"}
    if response_format == "xml":
        xml = dicttoxml.dicttoxml(response_data, custom_root='response', attr_type=False)
        dom = parseString(xml)
        xml_str = dom.toprettyxml()
        return Response(xml_str, mimetype='application/xml'), 201
    else:
        return make_response(jsonify(response_data), 201)


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

    rows_affected = cur.rowcount
    cur.close()
    response_format = request.args.get('format', 'json')
    return format_response({"message": f"Employee '{id}' Updated Successfully", "rows_affected": f"Rows Affected: {rows_affected}"}, response_format)


@app.route("/employee/<int:id>", methods=["DELETE"])
def delete_employee(id):
    # Deletes Employee from the Database
    cur = mysql.connection.cursor()
    cur.execute(f"""DELETE FROM employee where employee_id = {id}""")
    mysql.connection.commit()

    rows_affected = cur.rowcount
    cur.close()
    response_format = request.args.get('format', 'json')
    return format_response({"message": f"Employee '{id}' Deleted Successfully", "rows_affected": f"Rows Affected: {rows_affected}"}, response_format)


@app.route("/employee/format", methods=["GET"])
def get_params():
    fmt = request.args.get('format', 'json')
    foo = request.args.get('aaaa')
    return make_response(jsonify({"format": fmt, "foo": foo}), 200)


if __name__ == "__main__":
    app.run(debug=True)