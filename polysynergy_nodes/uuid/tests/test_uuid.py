import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.uuid import UUIDv4


class TestUUIDv4:
    def test_uuid_generation(self):
        node = UUIDv4()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should generate a valid UUID string
        assert isinstance(node.true_path, str)
        assert node.false_path is False
        
        # Should be a valid UUID format
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 4

    def test_uuid_uniqueness(self):
        """Test that multiple calls generate different UUIDs."""
        uuids = set()
        
        for _ in range(10):
            node = UUIDv4()
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            uuids.add(node.true_path)
        
        # All UUIDs should be unique
        assert len(uuids) == 10

    def test_uuid_format(self):
        node = UUIDv4()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should match UUID format pattern (8-4-4-4-12)
        parts = node.true_path.split('-')
        assert len(parts) == 5
        assert len(parts[0]) == 8
        assert len(parts[1]) == 4
        assert len(parts[2]) == 4
        assert len(parts[3]) == 4
        assert len(parts[4]) == 12

    def test_uuid_hex_characters(self):
        node = UUIDv4()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should only contain hex characters and dashes
        uuid_no_dash = node.true_path.replace('-', '')
        assert all(c in '0123456789abcdef' for c in uuid_no_dash)

    def test_multiple_executions(self):
        """Test that the same node can be executed multiple times."""
        node = UUIDv4()
        
        # Execute multiple times and collect results
        results = []
        for _ in range(5):
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All should be valid and different
        assert len(set(results)) == 5
        for result in results:
            uuid.UUID(result)  # Should not raise exception