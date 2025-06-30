import random
import boto3
import os

# Import environment variables
MODEL_ID = "amazon.nova-reel-v1:0"
S3_DESTINATION_BUCKET = os.environ.get("S3_BUCKET")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

async def create_video(prompt):
    """
    Creates video using Amazon Nova Reel model.

    :param prompt: Prompt for creation of the video
    :return: URL for the file
    """

    # Initiate Bedrock Client
    bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION, aws_access_key_id =AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Set video parameters
    model_input = {
        "taskType": "TEXT_VIDEO",
        "textToVideoParams": {"text": prompt},
        "videoGenerationConfig": {
            "durationSeconds": 6,
            "fps": 24,
            "dimension": "1280x720",
            "seed": random.randint(0, 2147483648)
        }
    }

    # Invoke the model to start creation
    invocation = bedrock_runtime.start_async_invoke(
        modelId=MODEL_ID,
        modelInput=model_input,
        outputDataConfig={"s3OutputDataConfig": {"s3Uri": f"s3://{S3_DESTINATION_BUCKET}"}}
    )

    # Get invocation Arn and S3 folder
    invocation_arn = invocation["invocationArn"]
    s3_prefix = invocation_arn.split('/')[-1]

    # Initiate S3 Client
    s3_client = boto3.client('s3', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                             endpoint_url=f'https://s3.{AWS_REGION}.amazonaws.com')

    # Get pre-signed URL for the video to be generated
    url = s3_client.generate_presigned_url('get_object',
                                           Params={'Bucket': S3_DESTINATION_BUCKET,
                                                   'Key': f"{s3_prefix}/output.mp4"},
                                           ExpiresIn=7200)

    return url