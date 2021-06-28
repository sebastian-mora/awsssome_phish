
import boto3
import botocore
from os import environ

def check_token(sso_oidc_client, oidc_application, device_code):

    try:
        # print( oidc_application, device_code)
        token_response = sso_oidc_client.create_token(
        clientId=oidc_application[0],
        clientSecret=oidc_application[1],
        grantType="urn:ietf:params:oauth:grant-type:device_code",
        deviceCode=device_code
        )
        aws_sso_token = token_response.get('accessToken')
        return aws_sso_token
    except botocore.exceptions.ClientError as e:
        print(e.response['Error'])
        if e.response['Error']['Code'] != 'AuthorizationPendingException':
            return None
        
        return None


#this will work but it is not the most optimizable. Table query, then pass in filter parameter. Check to see if false
def get_sessions():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sessionTable')
    return table.scan()['Items'] 

def update_session_token(deviceCode, session_token):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sessionTable')


    # get item
    response = table.get_item(Key={'deviceCode': deviceCode})
    item = response['Item']

    item['token'] = session_token
    item['sessionCaptured'] = True

    table.put_item(Item=item)

    return True


def main(event, context):
    sso_oidc_client = boto3.client('sso-oidc', region_name=environ['REGION'])
    for session in get_sessions():
        
        if session['sessionCaptured'] is False:
            oicd_app = session['oidc_app']
            device_code_app = session['deviceCode']
            token = check_token(sso_oidc_client, oicd_app, device_code_app)
            if token: 
                print("GOT A HIT")
                update_session_token(device_code_app,token) 
            
    response = {
        "statusCode": 200
    }

    return response
