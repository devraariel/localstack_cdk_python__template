import json
import boto3
import os
def get_table_data(table_name):
    users = []
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1', endpoint_url="http://localhost:4566")
    table = dynamodb.Table(table_name)
    response = table.scan()
    users.extend(response.get('Items', []))
    return users
#    data = response['Items']
#    #while 'LastEvaluatedKey' in response:
#    #   response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
#    #   data.extend(response['Items'])
#    return data

def events_handler(events, context):
    print("Starting events_handler")
    env = os.environ
    users_table_name = env["USERS_TABLE_NAME"]
    users = get_table_data(users_table_name)
    body = events['body']
    path = events['path']
    http_method = events['httpMethod']
    res_body = { "path":  path, "http_method": http_method, 'body': body, "users_table": users_table_name, "users": users }
    return {
        'statusCode': 200,
        'body': json.dumps(res_body)
    }