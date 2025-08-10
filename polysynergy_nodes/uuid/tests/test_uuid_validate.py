import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.uuid_validate import UUIDValidate


class TestUUIDValidate:
    def test_valid_uuid_v4(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = str(uuid.uuid4())
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.version == 4
        assert node.false_path is False

    def test_valid_uuid_v1(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = str(uuid.uuid1())
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.version == 1
        assert node.false_path is False

    def test_valid_uuid_v5(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        test_uuid = str(uuid.uuid5(uuid.NAMESPACE_DNS, "test"))
        node.uuid_string = test_uuid
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.version == 5
        assert node.false_path is False

    def test_check_specific_version_match(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = str(uuid.uuid4())
        node.check_version = 4
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.version == 4
        assert node.false_path is False

    def test_check_specific_version_mismatch(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = str(uuid.uuid4())
        node.check_version = 1  # Expecting v1 but got v4
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 4
        assert node.false_path is False

    def test_invalid_uuid_format(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = "not-a-valid-uuid"
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 0
        assert node.false_path is False  # Not an error, just invalid

    def test_malformed_uuid(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = "123e4567-e89b-12d3-a456-42661417400"  # Missing one digit
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 0
        assert node.false_path is False

    def test_uuid_with_wrong_separators(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = "123e4567_e89b_12d3_a456_426614174000"  # Underscores instead of dashes
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 0
        assert node.false_path is False

    def test_valid_nil_uuid(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = "00000000-0000-0000-0000-000000000000"
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.false_path is False
        # Nil UUID doesn't have a version
        assert node.version is None or node.version == 0

    def test_uppercase_uuid(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        test_uuid = str(uuid.uuid4()).upper()
        node.uuid_string = test_uuid
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is True
        assert node.version == 4
        assert node.false_path is False

    def test_non_string_input(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = 123
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 0
        assert "UUID must be a string" in str(node.false_path)

    def test_empty_string(self):
        node = UUIDValidate()
        node.true_path = False
        node.false_path = False
        node.version = 0
        node.uuid_string = ""
        node.check_version = 0
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert node.version == 0
        assert node.false_path is False