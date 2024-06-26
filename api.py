from flask import Flask, make_response, jsonify, request, Response, render_template
from flask_mysqldb import MySQL
import dicttoxml
from xml.dom.minidom import parseString
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps


app = Flask(__name__)
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""       # Enter Your SQL Password Here
app.config["MYSQL_DB"] = "emp_dep_db"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)


app.config['JWT_SECRET_KEY'] = 'your_secret_key'

token_lock = True

############################################################


@app.route("/", methods=["GET"])
def front():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == 'admin' and password == 'admin':
        token = jwt.encode({'exp': datetime.now(timezone.utc) + timedelta(minutes=30)}, app.config['JWT_SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('Could Not Verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not token_lock:
            return f(*args, **kwargs)
        
        token = request.args.get('token')
        if not token:
            return jsonify({'message': 'Token is Missing!'}), 403
        try:
            decoded_token = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is Invalid!'}), 403
        return f(*args, **kwargs)
    return decorated


############################################################


def data_fetch(query, params=None):
    cur = mysql.connection.cursor()
    if params:
        cur.execute(query, params)
    else:
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


############################################################


@app.route("/employee", methods=["GET"])
@token_required
def get_employee():
    # Get All Employee Details
    data = data_fetch("""SELECT * FROM employee""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)


@app.route("/employee/<int:id>", methods=["GET"])
@token_required
def get_employee_by_id(id):
    # Get Employee by Employee ID
    data = data_fetch(f"""SELECT * FROM employee WHERE employee_id = {id}""")
    response_format = request.args.get('format', 'json')
    return format_response(data, response_format)


@app.route("/employee/<int:id>/department", methods=["GET"])
@token_required
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
@token_required
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
@token_required
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
@token_required
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
@token_required
def get_params():
    fmt = request.args.get('format', 'json')
    return make_response(jsonify({"format": fmt}), 200)


############################################################


@app.route("/search", methods=["GET"])
@token_required
def search():
    return render_template("search.html")


@app.route("/search/results", methods=["GET"])
@token_required
def search_results():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    department_id = request.args.get('department_id')

    query = "SELECT * FROM employee WHERE 1=1"
    params = []

    if first_name:
        query += " AND first_name LIKE %s"
        params.append(f"%{first_name}%")
    if last_name:
        query += " AND last_name LIKE %s"
        params.append(f"%{last_name}%")
    if department_id:
        query += " AND department_id = %s"
        params.append(department_id)

    data = data_fetch(query, params)
    return render_template("search_results.html", results=data)


############################################################


if __name__ == "__main__":
    app.run(debug=True)