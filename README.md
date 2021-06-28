



# aws_sso_phishing
AWS SSO phishing infrastructure 


## Demo

https://user-images.githubusercontent.com/24581748/123670450-1471ec80-d7f2-11eb-8d6d-62fa4253ad46.MOV

## How it works 

This method was originally posted in a blog by XXX.

When a user visits / of the url a lambda function starts an sso-oicd authentication. Here a sso URL with a user token is generated and the victim is automatically redirected to. The device tokens or (session) will be stored in a DynamoDb table for later. To bypass the 6 min login URL expire, URLs are generated "Just In Time" when the user visits the attacker URL. 

Once redirected there will be an AWS SSO prompt asking the user to accept. If the user accepts then the sso-oicd device client tokens become valid and can be used to generate a session token to authenticate to the environment. There is another function that is triggered by cloudwatch that monitors these tokens. Once a token becomes active it the function generates a valid session token and the DB is updated.



## Usage

The setup of this tool is nearly completely automated. Deploy the framework with serverless and take note of the outputs. 

Once deployed you will get your deployment endpoint as well as an API key to access the routes. 

A lambda function will poll sessions for any sessions accepted by the user. Once a session is accepted email will be sent via an SNS topic to the email specified in config.js. You may also use the available API endpoints to grab the information from DynamoDb. Finally, you can use the console directly to view the DynamoDb table.


## How it works

### Routes
    * / 

    This route is the main redirect route. Here your victims will automatically be redirected to an AWS SSO auth prompt. On click, a session will be stored in DynamoDb. If the user clicks accept on the prompt another function will poll the session and attempt to generate session tokens.

    * /getClicks

    This route returns all active sessions from "clicks" this includes sessions that have not been accepted by the user. 

    * /getTokens

    This route returns all sessions that have valid session tokens. Meaning the user has clicked the link and accept the auth prompt. These tokens can be used to auth to the SSO org.

## Requirments 

* Nodejs
* Python3


## Install 

1. Install serverless framework 
    `npm install serverless`

2. Add notification email address to `config.js`

3. Specific the SSO URL and region in `config.js`

3. Deploy the API
    `sls deploy

4. Accept the invitation to the SNS notification

5. Take note of the API Key and deployed endpoints. 

    At this stage, you will want to consider adding a custom domain name to your deployment. 
