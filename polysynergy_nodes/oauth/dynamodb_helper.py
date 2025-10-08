"""
Helper functions for DynamoDB operations in OAuth nodes
"""
import os
import boto3
import logging

logger = logging.getLogger(__name__)

_dynamodb_table_cache = None

def get_oauth_dynamodb_table():
    """
    Get or create the OAuthTokens DynamoDB table.

    This function will:
    1. Try to get the existing table
    2. If table doesn't exist, create it automatically
    3. Return the table resource for operations

    Returns:
        boto3.Table or None: The DynamoDB table resource, or None if failed
    """
    global _dynamodb_table_cache

    # Return cached table if available
    if _dynamodb_table_cache is not None:
        return _dynamodb_table_cache

    try:
        dynamodb = boto3.resource(
            "dynamodb",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "eu-central-1"),
        )

        table_name = "OAuthTokens"
        table = dynamodb.Table(table_name)

        # Check if table exists, create if not
        try:
            table.load()  # This will raise an exception if table doesn't exist
            logger.info(f"DynamoDB table {table_name} exists")
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            logger.info(f"Creating DynamoDB table {table_name}")

            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'node_id',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'node_id',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST',  # On-demand pricing

                # Add TTL for auth codes (optional)
                # This allows automatic cleanup of expired auth codes
                StreamSpecification={
                    'StreamEnabled': False,
                },
            )

            # Wait for table to be created
            logger.info(f"Waiting for DynamoDB table {table_name} to be created...")
            table.wait_until_exists()
            logger.info(f"DynamoDB table {table_name} created successfully")

        # Cache the table for future use
        _dynamodb_table_cache = table
        return table

    except Exception as e:
        logger.error(f"Failed to get/create DynamoDB table: {e}")
        return None

def clear_table_cache():
    """Clear the cached table (useful for testing)"""
    global _dynamodb_table_cache
    _dynamodb_table_cache = None