import os
from polysynergy_node_runner.setup_context.node import Node
from polysynergy_node_runner.setup_context.node_decorator import node
from polysynergy_node_runner.setup_context.node_variable_settings import NodeVariableSettings
from polysynergy_nodes.ocr.services.textract import TextractService


@node(
    name="AWS Textract",
    category="file",
    icon='<svg width="24px" height="24px" stroke-width="1.5" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" color="#000000"><path d="M4 7H20" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M4 17H9" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M4 12H17.5C18.8807 12 20 13.1193 20 14.5V14.5C20 15.8807 18.8807 17 17.5 17H12.5" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path><path d="M15 15.5L12.5 17L15 18.5V15.5Z" stroke="#000000" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"></path></svg>'
)
class AWSTextract(Node):
    file: str = NodeVariableSettings(label="File", dock=True, has_in=True)
    public: bool = NodeVariableSettings(default=False, has_in=True, dock=True, info="The files are in the public S3 bucket?")
    detect_forms_tables: bool = NodeVariableSettings(label="Detect Forms & Tables", has_in=True, dock=True, default=False)

    extracted_text: str = NodeVariableSettings(label="Extracted Text", has_out=True)
    structured_data: dict = NodeVariableSettings(label="Structured Data (Forms/Tables)", has_out=True)

    project_id: str = os.getenv('PROJECT_ID')

    def execute(self):
        if not self.file:
            raise ValueError("No files provided for Textract processing.")

        files = self.file if isinstance(self.file, list) else [self.file]

        textract_service = TextractService()

        result = textract_service.extract_text(
            project_id=self.project_id,
            files=files,
            public=self.public,
            detect_forms_tables=self.detect_forms_tables,
        )

        print('TEXTRACT RESULT', result)

        self.extracted_text = result["extracted_text"]
        self.structured_data = result["structured_data"]

        return self