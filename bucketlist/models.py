"""user module"""

import datetime, random

class User():
    """applicaton user"""
    def __init__(self, user_id, first_name, last_name, email, password):
        self.user_id = user_id
        self.first_name =first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.buckets = dict()
    
    def create_bucket(self, name):
        bucket_id = self.__generate_key()
        bucket = Bucket(bucket_id, str(name))
        self.buckets[bucket_id] = bucket
        return bucket
    
    def edit_bucket(self, bucket_id, name):
        bucket = self.buckets[bucket_id]
        bucket.name = name
        self.buckets[bucket_id] = bucket

    def delete_bucket(self, bucket_id):
        size = len(self.buckets)
        if not bucket_id in self.buckets:
            raise ValueError() 
        del self.buckets[bucket_id]

    def __generate_key(self):
        """converts a string to a slug"""
        return str(random.randrange(100000, 1000000))

class Bucket():
    def __init__(self, bucket_id, name):
        self.bucket_id = bucket_id
        self.name = name
        self.items = dict()

    def create_item(self, title, description, target_date):
        item_id = self.__generate_key()
        item = BucketItem(title, description, target_date, item_id)
        self.items[item_id] = item
        return item

    def edit_item(self, item_id, title, description, target_date):
        if item_id in self.items:
            self.items[item_id].title = title
            self.items[item_id].description = description
            self.items[item_id].target_date = target_date

    def set_complete(self, item_id):
        if item_id in self.items:
            self.items[item_id].is_complete = True
    
    def set_incomplete(self, item_id):
        if item_id in self.items:
            self.items[item_id].is_complete = False

    def delete_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]  
            
    def __generate_key(self):
        """converts a string to a slug"""
        return str(random.randrange(100000, 1000000))

class BucketItem():
    def __init__(self, title, description, target_date, item_id=None):
        self.item_id = item_id
        self.title = title
        self.is_complete = False
        self.description = description
        self.target_date = target_date #date to accomplish task
        self.timestamp = str(datetime.datetime.today())

    
