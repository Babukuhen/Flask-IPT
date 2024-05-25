import unittest
import warnings
from api import app

# TESTING DOESN'T TAKE INTO ACCOUNT THE TOKEN REQUIREMENT
# MAKE SURE TO DISABLE TOKEN REQUIREMENT TO TEST PROPERLY

class MyAppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

        warnings.simplefilter("ignore", category=DeprecationWarning)

    def test_index_page(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<!DOCTYPE html>", response.data)
        self.assertIn(b"<title>Login</title>", response.data)
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
        new_employee = {"first_name": "Jane", "last_name": "Da", "department_id": 1}
        response = self.app.post("/employee", json=new_employee)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("Employee Added Successfully" in response.data.decode())
        print()
    
    def test_update_employee(self):
        updated_employee = {"first_name": "Jane", "last_name": "Smith", "department_id": 1}
        response = self.app.put("/employee/64", json=updated_employee)      # YOU CAN CHANGE ID 
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Employee '64' Updated Successfully" in response.data.decode())
        print()

    def test_delete_employee(self):
        response = self.app.delete("/employee/64")                          # YOU CAN CHANGE ID 
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Employee '64' Deleted Successfully" in response.data.decode())
        print()


if __name__ == "__main__":
    unittest.main()
