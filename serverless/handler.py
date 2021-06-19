# handler.py
# by Preston Hager

import json
import boto3
from uuid import uuid4

dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table('kbb-users')

def test(event, context):
    try:
        data = json.loads(event['body'])
    except:
        response = {
            "error": "Body was not JSON content."
        }
        return create_response(response, 400)
    if "user" not in data or "type" not in data:
        response = {
            "error": "JSON content did not contain key values."
        }
        return create_response(response, 400)
    if data["type"] == "test":
        response = {
            "message": "Test successful!"
        }
        return create_response(response, 200)
    # get the user id, find them in the table, and add a box.
    user_id = data["user"]
    query = users_table.get_item(Key={'user_id': user_id})
    item_uuid = uuid4().hex
    box_item = {"uuid": item_uuid, "name": "Mystery Box", "description": "Open to reveal whatever might be inside!", "amount": 1, "item": "mystery_box"}
    response = {
        "message": "Success!"
    }
    if "Item" not in query:
        users_table.put_item(Item={
            "user_id": user_id,
            "relationships": {'current': {}},
            "inventory": {item_uuid: box_item}
        })
        return create_response(response, 200)
    found_item = False
    user_data = query["Item"]
    for i in user_data["inventory"]:
        item = user_data["inventory"][i]
        if item['item'] == "mystery_box":
            item['amount'] = int(item['amount']) + 1
            found_item = True
            break
    if not found_item:
        user_data["inventory"][item_uuid] = box_item
    users_table.update_item(Key={'user_id': user_id},
        UpdateExpression="set inventory = :i",
        ExpressionAttributeValues={
            ':i': user_data["inventory"]
        })
    return create_response(response, 200)

def create_response(body, code=200):
    return {
        "statusCode": code,
        "body": json.dumps(body)
    }
