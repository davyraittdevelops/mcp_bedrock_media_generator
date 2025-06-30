import boto3
import json
import os
import base64
import io

# Import environment variables
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
MODEL_ID = "amazon.nova-canvas-v1:0"
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

async def create_image(prompt,negative_prompt, quality, width, height, seed_value):
    """
    Creates image using Amazon Nova Canvas model.

    :param prompt: Prompt for image.
    :param negative_prompt: What not to use in image.
    :param quality: Standard or premium quality
    :param width: Width of the picture
    :param height: Height of the picture.
    :param seed_value: Seed value for the picture
    :return: Base64 encoded image string
    """

    # Initiate Bedrock Client
    bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    # Set picture parameters
    model_input = json.dumps({
        "taskType": "TEXT_IMAGE",
        "textToImageParams": {
            "text": prompt,
            "negativeText": negative_prompt
        },
        "imageGenerationConfig": {
            "width": width,
            "height": height,
            "quality": quality,
            "cfgScale": 3,
            "seed": seed_value,
            "numberOfImages": 1
        }
    })

    # Invoke model
    response = bedrock.invoke_model(
        body=model_input,
        modelId=MODEL_ID,
        accept="application/json",
        contentType="application/json"
    )

    # Read the response body
    response_body = json.loads(response.get("body").read())

    # Extract and return the first image
    base64_image = response_body.get("images")[0]

    return base64_image