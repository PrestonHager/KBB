# database_manager.py
# by Preston Hager

import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb', region_name="us-west-2")

class DatabaseManager:
    DEFAULT_PEOPLE = []

    def __init__(self, table):
        self.table = dynamodb.Table(table)

    def get_user(self, user_id):
        query = self.table.get_item(Key={'user_id': user_id})
        if "Item" not in query:
            return None
        return query["Item"]

    def get_guild(self, guild_id):
        query = self.table.get_item(Key={'guild_id': guild_id})
        if "Item" not in query:
            return None
        if 'people' not in query["Item"]:
            query["Item"]['people'] = self.DEFAULT_PEOPLE
        return query["Item"]

    def new_user(self, user_id):
        new_user = {
            'user_id': user_id,
            "relationships": {'current': {}},
            "inventory": {}
        }
        self.table.put_item(Item=new_user)
        return new_user

    def new_guild(self, guild_id):
        new_guild = {
            'guild_id': guild_id,
            "prefix": ';',
            "people": self.DEFAULT_PEOPLE
        }
        self.table.put_item(Item=new_guild)
        return new_guild

    def put_user(self, user_id, **kwargs):
        if "user" in kwargs:
            query = self._update_item('user_id', user_id, "set relationships = :r, inventory = :i", {":r": kwargs['user']["relationships"], ":i": kwargs['user']["inventory"]})
        elif "relationships" in kwargs:
            query = self._update_item('user_id', user_id, "set relationships = :r", {":r": kwargs["relationships"]})
        elif "inventory" in kwargs:
            query = self._update_item('user_id', user_id, "set inventory = :i", {":i": kwargs["inventory"]})

    def put_guild(self, guild_id, **kwargs):
        if "guild" in kwargs:
            query = self._update_item('guild_id', guild_id, "set prefix = :p", {":p": kwargs['guild']["prefix"]})
        elif "prefix" in kwargs:
            query = self._update_item('guild_id', guild_id, "set prefix = :p", {":p": kwargs["prefix"]})
        elif "people" in kwargs:
            query = self._update_item('guild_id', guild_id, "set people = :p", {":p": kwargs["people"]})

    def _update_item(self, key, user_id, expression, values):
        query = self.table.update_item(Key={key: user_id}, UpdateExpression=expression, ExpressionAttributeValues=values, ReturnValues="ALL_NEW")
        return query

__all__ = ["DatabaseManager"]
