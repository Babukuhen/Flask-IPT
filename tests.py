import unittest
import warnings
from api import app


class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")
        print()

    def test_get_employee(self):
        response = self.app.get("/employee")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("John" in response.data.decode())
        print()

    def test_get_employee_by_id(self):
        response = self.app.get("/employee/20")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Scott" in response.data.decode())
        print()

    def test_get_deptloc_by_empid(self):
        response = self.app.get("/employee/20/department")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Savannah" in response.data.decode())
        print()

    def test_add_employee(self):
        new_employee = {"first_name": "Jane", "last_name": "Doe", "department_id": 1}
        response = self.app.post("/employee", json=new_employee)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Employee Added Successfully" in response.data.decode())
        print()
    
    def test_update_employee(self):
        updated_employee = {"first_name": "Jane", "last_name": "Smith", "department_id": 1}
        response = self.app.put("/employee/21", json=updated_employee)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Employee '21' Updated Successfully" in response.data.decode())
        print()

    def test_delete_employee(self):
        response = self.app.delete("/employee/21")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Employee '21' Deleted Successfully" in response.data.decode())
        print()


if __name__ == "__main__":
    unittest.main()
