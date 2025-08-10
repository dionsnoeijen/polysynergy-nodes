import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.deterministic import DeterministicUUID


class TestDeterministicUUID:
    def test_deterministic_generation(self):
        node = DeterministicUUID()
        node.true_path = False
        node.false_path = False
        node.input_string = "test input"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        # Should generate a valid UUID string
        assert isinstance(node.true_path, str)
        assert node.false_path is False
        
        # Should be a valid UUID v5
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 5

    def test_deterministic_consistency(self):
        """Test that same input always generates same UUID."""
        input_text = "consistent input"
        results = []
        
        for _ in range(5):
            node = DeterministicUUID()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be identical
        assert len(set(results)) == 1
        assert all(r == results[0] for r in results)

    def test_different_inputs_different_outputs(self):
        """Test that different inputs generate different UUIDs."""
        inputs = ["input1", "input2", "input3"]
        results = []
        
        for input_text in inputs:
            node = DeterministicUUID()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be different
        assert len(set(results)) == 3

    def test_different_namespaces(self):
        """Test that different namespaces generate different UUIDs for same input."""
        namespaces = ["DNS", "URL", "OID", "X500"]
        results = []
        
        for ns in namespaces:
            node = DeterministicUUID()
            node.true_path = False
            node.false_path = False
            node.input_string = "same input"
            node.namespace = ns
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be different
        assert len(set(results)) == 4

    def test_case_insensitive_namespace(self):
        """Test that namespace is case-insensitive."""
        input_text = "test input"
        
        node1 = DeterministicUUID()
        node1.true_path = False
        node1.false_path = False
        node1.input_string = input_text
        node1.namespace = "DNS"
        asyncio.run(node1.execute())
        
        node2 = DeterministicUUID()
        node2.true_path = False
        node2.false_path = False
        node2.input_string = input_text
        node2.namespace = "dns"
        asyncio.run(node2.execute())
        
        # Should generate same UUID
        assert node1.true_path == node2.true_path

    def test_invalid_namespace_defaults_to_dns(self):
        """Test that invalid namespace defaults to DNS."""
        node1 = DeterministicUUID()
        node1.true_path = False
        node1.false_path = False
        node1.input_string = "test input"
        node1.namespace = "INVALID"
        asyncio.run(node1.execute())
        
        node2 = DeterministicUUID()
        node2.true_path = False
        node2.false_path = False
        node2.input_string = "test input"
        node2.namespace = "DNS"
        asyncio.run(node2.execute())
        
        # Should generate same UUID (defaulted to DNS)
        assert node1.true_path == node2.true_path

    def test_empty_string_input(self):
        node = DeterministicUUID()
        node.true_path = False
        node.false_path = False
        node.input_string = ""
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        # Should still generate a valid UUID
        assert isinstance(node.true_path, str)
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 5

    def test_non_string_input(self):
        node = DeterministicUUID()
        node.true_path = False
        node.false_path = False
        node.input_string = 123  # Not a string
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Input must be a string" in str(node.false_path)

    def test_unicode_input(self):
        node = DeterministicUUID()
        node.true_path = False
        node.false_path = False
        node.input_string = "héllo wörld 🚀"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        # Should handle unicode correctly
        assert isinstance(node.true_path, str)
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 5