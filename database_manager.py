# database_manager.py
# by Preston Hager

import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')

class DatabaseManager:
    def __init__(self):
        self.table = dynamodb.Table('kbb-users')

__all__ = ["DatabaseManager"]
