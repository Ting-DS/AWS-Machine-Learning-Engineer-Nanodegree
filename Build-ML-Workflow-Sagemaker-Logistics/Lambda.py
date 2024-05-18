"""
Lambda Function 1: getImage-lambdaFunction

A lambda function that copies an object from S3, base64 encodes it, and 
then return it (serialized data) to step function as `image_data` in an event.
"""

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event["image_url"]
    bucket = event["s3_bucket"]

    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket,key,"/tmp/image.png")
    
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        "image_data": image_data,
        "s3_bucket": bucket,
        "s3_key": key,
        "inferences": []
    }

"""
Lambda Function 2: getInference-lambdaFunction

A lambda function that is responsible for the classification part. It takes the image output from the 
lambda 1 function, decodes it, and then pass inferences back to the the Step Function
"""

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2023-10-10-06-28-45-621"

runtime_client = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])

    # Instantiate a Predictor
    predictor = runtime_client.invoke_endpoint(
        EndpointName = ENDPOINT,
        Body = image,
        ContentType = 'image/png'
    )

    # Make a prediction:
    inferences = json.loads(predictor['Body'].read().decode('utf-8'))

    return {
        'statusCode': 200,
        'inferences': inferences
    }

"""
Lambda Function 3: getResult-lambdaFunction

A lambda function that takes the inferences from the Lambda 2 function output and filters low-confidence inferences
(above a certain threshold indicating success)
"""

import json

THRESHOLD = 0.93

def lambda_handler(event, context):

    # Grab the inferences from the event
    inferences = event['inferences']

    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = max(inferences)>=THRESHOLD

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }  
