import json
from threading import main_thread
import boto3
import os

def create_oidc_application(sso_oidc_client):
    print("Creating temporary AWS SSO OIDC application")
    client = sso_oidc_client.register_client(
        clientName='aws-org-mapper',
        clientType='public'
    )
    client_id = client.get('clientId')
    client_secret = client.get('clientSecret')
    return client_id, client_secret


def initiate_device_code_flow(sso_oidc_client, client_id, client_secret, start_url):
    print("Initiating device code flow")
    authz = sso_oidc_client.start_device_authorization(
        clientId=client_id,
        clientSecret=client_secret,
        startUrl=start_url
    )

    url = authz.get('verificationUriComplete')
    deviceCode = authz.get('deviceCode')
    return url, deviceCode


def create_device_code_url(sso_oidc_client, start_url):
    oidc_application = create_oidc_application(sso_oidc_client)
    url, device_code = initiate_device_code_flow(
        sso_oidc_client, oidc_application, start_url)
    return url, device_code, oidc_application

def main(event, context):

    START_URL = os.environ['START_URL']
    REGION = os.environ['REGION']
    sso = boto3.client('sso', region_name=REGION)

    url = create_device_code_url(sso, START_URL)
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": url
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

print(main(None, None))