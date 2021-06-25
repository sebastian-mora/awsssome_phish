import json
import boto3
import botocore
from os import environ


# Create dyamodb table 
# write loop

# test token active (wont work with mock data) 


# if active then publish message to sns 'sessionCaptured': False,

# update db table sessionCaptured timestamp

# triggered by clouwatch (this is in serverless documentiaon. Trigger every 1 min )

def check_token(sso_oidc_client, oidc_application, device_code):
    sso_token = ''
    print("Waiting indefinitely for user to validate the AWS SSO prompt...")
    try:
        token_response = sso_oidc_client.create_token(
        clientId=oidc_application[0],
        clientSecret=oidc_application[1],
        grantType="urn:ietf:params:oauth:grant-type:device_code",
        deviceCode=device_code
        )
        aws_sso_token = token_response.get('accessToken')
        return aws_sso_token
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] != 'AuthorizationPendingException':
            pass


#this will work but it is not the most optimizable. Table query, then pass in filter parameter. Check to see if false
def get_sessions():
    dynamodb = boto3.resource('dynamodb', region_name=environ['REGION'])
    table = dynamodb.Table('sessionTable')
    return table.scan()['Items'] 

def update_session_token(deviceCode, token):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('sessionTable')

    data={
        'token': token,
    }

    table.update_item(
        Item=data, 
        Key = deviceCode
    )

    return data


def main(event, context):
    sso_oidc_client = boto3.client('sso-oidc', region_name=environ['REGION'])
    for session in get_sessions():
        
        if session['sessionCaptured'] is False:
            print(session)
            oicd_app = session['oidc_app']
            device_code_app = session['deviceCode']
            token = check_token(sso_oidc_client, oicd_app, device_code_app)
            if token: 
                update_session_token(device_code_app,token) 
                #send_alert()
            
    response = {
        "statusCode": 200
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
main(1,1)