import unittest
from bucketlist.appmanager import ApplicationManager
from bucketlist.models import User, BucketItem

class Test(unittest.TestCase):
    def setUp(self):
        self.app = ApplicationManager()
        first_name = "John"
        last_name = "Doe"
        email = "john@example.com"
        password = "the_strongest_password"
        self.user1 = self.app.create_user(first_name, last_name, email, password)
        self.java_bucket = self.user1.create_bucket("Java")
        self.php_bucket = self.user1.create_bucket("PHP")

    def test_user_can_create_bucket(self):
        self.assertEqual(2, len(self.user1.buckets))
        self.assertTrue(self.php_bucket, User)

    def test_delete_bucket(self):
        bucket_size = len(self.user1.buckets)
        self.user1.delete_bucket(self.php_bucket.bucket_id)
        self.assertEqual( bucket_size - 1, len(self.user1.buckets))

    def test_edit_bucket(self):
        bucket_id = self.php_bucket.bucket_id
        self.user1.edit_bucket(bucket_id, "PHP 7.0")
        self.assertEqual("PHP 7.0", self.php_bucket.name)

    def test_can_create_bucket_item(self):
        result = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.assertEqual(1, len(self.java_bucket.items))
        self.assertTrue(isinstance(result, BucketItem))

    def test_can_edit_bucket_item(self):
        item = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.java_bucket.edit_item("OOP", "Classes", "2017-08-12")
