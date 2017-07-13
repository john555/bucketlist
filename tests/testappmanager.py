import unittest
from bucketlist.appmanager import ApplicationManager
from bucketlist.models import User

class Test(unittest.TestCase):
    def setUp(self):
        self.app = ApplicationManager()
        first_name = "John"
        last_name = "Doe"
        email = "john@example.com"
        password = "the_strongest_password"
        self.user1 = self.app.create_user(first_name, last_name, email, password)
    
    def test_appication_can_add_user(self):
        self.assertEqual(1, len(self.app.users))

    def test_returns_user_object_on_create(self):
        self.assertTrue(isinstance(self.user1, User))

    def test_automatically_generates_user_id(self):
        self.assertTrue(len(self.user1.user_id) > 0)

    def test_raises_value_error_on_user_update(self):
        user_id = "some-non-existent-id"
        with self.assertRaises(ValueError):
            self.app.update_user(user_id, "Jane", "Muller")
    
    def test_raises_value_error_on_invalid_data_type(self):
        """tests if creating and updating user object raises ValueError on invalid inputs"""
        with self.assertRaises(ValueError):
            self.app.update_user(self.user1.user_id, "", "")
            self.app.update_user(self.user1.user_id, 0, 8)
            self.app.create_user("", "", "", "")
            self.app.create_user("", "", 9, "")

    def test_can_edit_user(self):
        user_id = self.user1.user_id
        updated_user = self.app.update_user(user_id, "Jane", "Muller")
        self.assertEqual("Jane", updated_user.first_name)
        self.assertEqual("Muller", self.app.users[user_id].last_name)
    
    def test_raises_error_on_user_delete(self):
        """check if error is raised on ApplicationManager.delete_user when key does not exist"""
        with self.assertRaises(ValueError):
            self.app.delete_user("no-id")

    def test_can_delete_user(self):
        total_users_num = len(self.app.users)
        self.app.delete_user(self.user1.user_id)
        self.assertEqual(0, total_users_num-1)
