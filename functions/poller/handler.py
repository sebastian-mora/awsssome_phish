import json


# Create dyamodb table 
# write loop

# test token active (wont work with mock data)


# if active then publish message to sns 

# update db table sessionCaptured timestamp

# triggered by clouwatch (this is in serverless documentiaon. Trigger every 1 min )


def main(event, context):

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
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
