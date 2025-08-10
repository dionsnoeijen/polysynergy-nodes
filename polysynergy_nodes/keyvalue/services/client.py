import boto3
import os

class DynamoDBClient:

    def __init__(self):
        is_lambda = os.getenv("AWS_EXECUTION_ENV") is not None

        if is_lambda:
            self.dynamodb = boto3.resource(
                "dynamodb",
                region_name=os.getenv("AWS_REGION", "eu-central-1"),
            )
        else:
            self.dynamodb = boto3.resource(
                "dynamodb",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_REGION", "eu-central-1"),
            )

    def get_table(self):
        return self.dynamodb.Table("user_key_value_store")