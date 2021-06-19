# database_manager.py
# by Preston Hager

import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')

class DatabaseManager:
    def __init__(self, table):
        self.table = dynamodb.Table(table)

    def get_user(self, user_id):
        query = self.table.get_item(Key={'user_id': user_id})
        if "Item" not in query:
            return None
        return query["Item"]

    def new_user(self, user_id):
        new_user = {
            'user_id': user_id,
            "relationships": {'current': {}},
            "inventory": {}
        }
        self.table.put_item(Item=new_user)
        return new_user

    def put_user(self, user_id, **kwargs):
        if "user" in kwargs:
            query = self._update_user(user_id, "set relationships = :r, inventory = :i", {":r": kwargs['user']["relationships"], ":i": kwargs['user']["inventory"]})
        elif "relationships" in kwargs:
            query = self._update_user(user_id, "set relationships = :r", {":r": kwargs["relationships"]})
        elif "inventory" in kwargs:
            query = self._update_user(user_id, "set inventory = :i", {":i": kwargs["inventory"]})

    def _update_user(self, user_id, expression, values):
        query = self.table.update_item(Key={'user_id': user_id}, UpdateExpression=expression, ExpressionAttributeValues=values, ReturnValues="ALL_NEW")

__all__ = ["DatabaseManager"]
