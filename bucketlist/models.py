"""user module"""

import datetime

class User():
    """applicaton user"""
    def __init__(self, user_id, first_name, last_name, email, password):
        self.user_id = user_id
        self.first_name =first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.buckets = list()
    
    def create_bucket(self, name):
        bucket = Bucket(name)
        self.buckets.append(bucket)
    
    def delete_bucket(self, index):
        size = len(self.buckets)

        if not (size > index + 1 or index < 0):
            raise ValueError() 
        del self.buckets[index]

class Bucket():
    def __init__(self, name):
        #self.bucket_id = 
        self.name = name
        self.items = list()

    def add_item(self, title, description, target_date):
        item = BucketItem(title, description, target_date)
        self.items.append(item)

class BucketItem():
    def __init__(self, title, description, target_date):
        #self.item_id = 
        self.title = title
        self.is_complete = False
        self.description = description
        self.target_date = target_date #date to accomplish task
        self.timestamp = str(datetime.datetime.today())
