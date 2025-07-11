import os
import boto3
import logging
import botocore.exceptions

logger = logging.getLogger(__name__)


class TextractService:
    def __init__(self):
        self.textract_client = boto3.client(
            "textract",
            region_name=os.getenv("AWS_REGION", "eu-central-1")
        )
        self.public_bucket = os.getenv("AWS_S3_PUBLIC_BUCKET_NAME")
        self.private_bucket = os.getenv("AWS_S3_PRIVATE_BUCKET_NAME")

    def extract_text(self, project_id: str, files: list[str], public: bool = False, detect_forms_tables: bool = False):
        if not files:
            raise ValueError("No files provided for Textract processing.")

        bucket_name = self.public_bucket if public else self.private_bucket
        extracted_texts = []
        structured_data_list = []

        for file in files:
            file_path = f"{project_id}/{file.strip()}"

            print(f"🧠 Initiating Textract for: Bucket={bucket_name} | Key={file_path} | Detect Forms & Tables={detect_forms_tables}")
            try:
                if detect_forms_tables:
                    response = self.textract_client.analyze_document(
                        Document={"S3Object": {"Bucket": bucket_name, "Name": file_path}},
                        FeatureTypes=["FORMS", "TABLES"]
                    )
                else:
                    response = self.textract_client.detect_document_text(
                        Document={"S3Object": {"Bucket": bucket_name, "Name": file_path}}
                    )

                extracted_text, structured_data = self._parse_textract_response(response)
                extracted_texts.append(extracted_text)
                structured_data_list.append(structured_data)

            except botocore.exceptions.ClientError as e:
                logger.error(f"🚫 Textract ClientError for file {file_path}: {e}")
                logger.error(f"📝 Full error response: {e.response}")
                extracted_texts.append("")
                structured_data_list.append({})

            except Exception as e:
                logger.exception(f"🔥 Unexpected Textract error for {file_path}: {e}")
                extracted_texts.append("")
                structured_data_list.append({})

        return {
            "extracted_text": "\n\n".join(extracted_texts),
            "structured_data": structured_data_list if detect_forms_tables else {},
        }

    @staticmethod
    def _parse_textract_response(response):
        extracted_text = []
        structured_data = {"Forms": [], "Tables": []}

        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                extracted_text.append(block["Text"])
            elif block["BlockType"] == "KEY_VALUE_SET" and "EntityTypes" in block and "KEY" in block["EntityTypes"]:
                structured_data["Forms"].append({
                    "Key": block.get("Text", ""),
                    "Value": block.get("Value", "")
                })
            elif block["BlockType"] == "TABLE":
                structured_data["Tables"].append(block)

        return "\n".join(extracted_text), structured_data