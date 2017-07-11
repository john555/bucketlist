"""This module creates a new user instance and stores it in an in-memory disctionary."""
import random
from bucketlist.models import User

class ApplicationManager():
    """creates """
    def __init__(self):
        self.users = dict()
    def create_user(self, first_name, last_name, email, password):
        """creates a new User object and stores it in self.users"""
        if not self.__is_valid_input(first_name, str):
            raise ValueError()
        if not self.__is_valid_input(first_name, str):
            raise ValueError()
        if not self.__is_valid_input(last_name, str):
            raise ValueError()
        if not self.__is_valid_input(email, str):
            raise ValueError()
        if not self.__is_valid_input(password, str):
            raise ValueError()

        user_id = self.__generate_user_id()
        user = User(user_id=user_id, first_name=first_name, last_name=last_name, email=email, password=password)
        self.users[user_id] = user
        return user

    def update_user(self, user_id, first_name, last_name):
        """changes a user object's first_name and last_name properties"""
        if not self.__is_valid_input(first_name, str):
            raise ValueError()

        if not self.__is_valid_input(first_name, str):
            raise ValueError()

        if not user_id in self.users:
            raise ValueError()
        user = self.users[user_id]
        user.first_name = first_name
        user.last_name = last_name
        self.users[user_id] = user
        return user

    def delete_user(self, user_id):
        """deletes a User object from"""
        if not user_id in self.users:
            raise ValueError()
        del self.users[user_id]

    def __generate_user_id(self):
        """returns random string to be used as a key in the self.users dictionary"""
        random.seed(2)
        return str(random.randrange(100000, 1000000))

    def __is_valid_input(self, value, valid_type):
        """check if input is of valid type"""
        if not isinstance(value, str):
            return isinstance(value, valid_type)
        else:
            return not len(value) == 0 
