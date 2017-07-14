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
        self.java_bucket.edit_item(item.item_id, "Hiking", "Classes", "2017-08-12")
        self.assertEqual("Hiking", item.title)
        self.assertEqual("Classes", item.description)

    def test_can_checkoff_finished_items(self):
        item = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.java_bucket.set_complete(item.item_id)
        self.assertTrue(self.java_bucket.items[item.item_id].is_complete)

    def test_can_indicate_finished_items(self):
        item = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.java_bucket.set_complete(item.item_id)
        self.assertTrue(self.java_bucket.items[item.item_id].is_complete)

    def test_can_indicate_unfinished_items(self):
        item = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.java_bucket.set_complete(item.item_id)
        self.java_bucket.set_incomplete(item.item_id)
        self.assertFalse(self.java_bucket.items[item.item_id].is_complete)
    
    def test_can_delete_item_from_bucket(self):
        item = self.java_bucket.create_item("OOP", "", "2017-08-12")
        self.java_bucket.delete_item(item.item_id)
        self.assertFalse(item.item_id in self.java_bucket.items)
    
