
#  awsssome_phish

This method was originally posted in a [blog](https://blog.christophetd.fr/phishing-for-aws-credentials-via-aws-sso-device-code-authentication) by Christophe Tafani-Dereeper. This tool serves as an implementation of their work. 

When a user visits `/` of the phishing URL a lambda function starts sso-oicd authentication, a device authentication URL is generated and the victim is automatically redirected. To bypass the 6 min device authentication URL expiration, URLs are generated "Just In Time" when the user visits the phishing URL. 

Once redirected there will be an AWS SSO prompt asking the user to accept. If the user accepts then the ssso-oicd tokens become valid. Then a session token is generated and stored in the DynamoDb table, which can be accessed via the API.

## Demo

https://user-images.githubusercontent.com/24581748/123670450-1471ec80-d7f2-11eb-8d6d-62fa4253ad46.MOV

## How it works

The setup of this tool is nearly automated. Deploy the framework with serverless and take note of the outputs. 

Once deployed you will get your deployment endpoint as well as an API key to access the protected routes. 

If you would like to add a custom domain to the API endpoint you must configure that manually in AWS.

## Requirments 

* Nodejs
* Python3

## Install 

1. Install serverless framework 
    `npm install serverless`

2. Specific the SSO URL and SSO Region in `config.js`

3. Deploy the API
    `sls deploy`

4. Take note of the API Key and deployed endpoints. 

    At this stage, you will want to consider adding a custom domain name to your deployment. 


## Usage

Once deployed you will have an API gateway endpoint. The root `/` will automatically start a device auth and redirect the victim to log in. You can periodically check `/getClicks` to see if anyone has interacted with the URL and `/getTokens` to see if any valid sessions have been captured. 

If you wish to directly generate a device authentication URL you can do that with `/createDeviceUrl`. Note: URLs are only valid for 6 minutes. It is recommended to use the redirect method. 



### Routes

| Route | Description | API Key Required |
| --- | --- | --- |
| `/(?v=base64_victim_name)` | Main redirect route. Victims will be redirected to an SSO auth prompt. Appending the base64 v= will tag the created URL with the victim's name. This allows you to track links for specific users. | False |
| `/getClicks` | Returns all active sessions from "clicks" this includes sessions that have not been accepted by the user. | True |
| `/getTokens` | Returns all sessions that have valid session tokens. Meaning the user has clicked the link and accept the auth prompt. These tokens can be used to auth to the SSO org. | True |
| `/createDeviceUrl(?v=base64_victim_name)` | Returns a device URL. This allows you to create an auth link directly if you wish to use the aws domain `device.sso.<region>.amazonaws.com`. Device URLs are valid for 6 minutes before they expire. Appending the base64 v= will tag the created URL with the victim's name. This allows you to track links for specific users.  | True |


