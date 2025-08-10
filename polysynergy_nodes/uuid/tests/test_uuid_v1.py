import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.uuid_v1 import UUIDv1


class TestUUIDv1:
    def test_uuid_v1_generation(self):
        node = UUIDv1()
        node.true_path = False
        node.false_path = False
        asyncio.run(node.execute())
        
        # Should generate a valid UUID string
        assert isinstance(node.true_path, str)
        assert node.false_path is False
        
        # Should be a valid UUID v1
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 1

    def test_uuid_v1_format(self):
        node = UUIDv1()
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

    def test_uuid_v1_temporal_ordering(self):
        """Test that UUID v1s generated in sequence are temporally ordered."""
        uuids = []
        
        for _ in range(5):
            node = UUIDv1()
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            uuids.append(uuid.UUID(node.true_path))
        
        # Extract timestamps from UUID v1s
        timestamps = [u.time for u in uuids]
        
        # Timestamps should be in ascending order (or very close)
        # Allow for some tolerance due to rapid generation
        for i in range(1, len(timestamps)):
            assert timestamps[i] >= timestamps[i-1] or abs(timestamps[i] - timestamps[i-1]) < 100

    def test_uuid_v1_uniqueness(self):
        """Test that multiple calls generate different UUIDs."""
        uuids = set()
        
        for _ in range(10):
            node = UUIDv1()
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            uuids.add(node.true_path)
        
        # All UUIDs should be unique
        assert len(uuids) == 10

    def test_uuid_v1_mac_consistency(self):
        """Test that UUID v1s from same machine have consistent node info."""
        uuids = []
        
        for _ in range(3):
            node = UUIDv1()
            node.true_path = False
            node.false_path = False
            asyncio.run(node.execute())
            uuids.append(uuid.UUID(node.true_path))
        
        # All UUIDs should have the same node (MAC address) component
        nodes = [u.node for u in uuids]
        assert len(set(nodes)) == 1  # All should be the same