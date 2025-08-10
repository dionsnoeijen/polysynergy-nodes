import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.uuid_nil import UUIDNil


class TestUUIDNil:
    def test_nil_uuid_generation(self):
        node = UUIDNil()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should generate the nil UUID
        expected_nil = "00000000-0000-0000-0000-000000000000"
        assert node.true_path == expected_nil
        assert node.false_path is False

    def test_nil_uuid_consistency(self):
        """Test that multiple calls always return the same nil UUID."""
        results = []
        
        for _ in range(5):
            node = UUIDNil()
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be identical
        assert len(set(results)) == 1
        assert results[0] == "00000000-0000-0000-0000-000000000000"

    def test_nil_uuid_is_valid_uuid(self):
        node = UUIDNil()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should be parseable as a valid UUID
        parsed = uuid.UUID(node.true_path)
        assert str(parsed) == "00000000-0000-0000-0000-000000000000"

    def test_nil_uuid_format(self):
        node = UUIDNil()
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
        
        # All parts should be zeros
        assert all(part == "0" * len(part) for part in parts)

    def test_nil_uuid_all_zeros(self):
        node = UUIDNil()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Remove dashes and verify all zeros
        uuid_no_dash = node.true_path.replace('-', '')
        assert uuid_no_dash == "0" * 32
        assert len(uuid_no_dash) == 32

    def test_nil_uuid_properties(self):
        node = UUIDNil()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        parsed = uuid.UUID(node.true_path)
        
        # Nil UUID should have specific properties
        assert parsed.int == 0
        assert parsed.hex == "00000000000000000000000000000000"