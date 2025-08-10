import asyncio
import uuid
import pytest
from polysynergy_nodes.uuid.uuid_from_string import UUIDFromString


class TestUUIDFromString:
    def test_sha1_method_consistency(self):
        """Test that SHA-1 method generates consistent UUIDs."""
        input_text = "test input"
        results = []
        
        for _ in range(3):
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "sha1"
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be identical
        assert len(set(results)) == 1
        # Should be valid UUID v5
        parsed = uuid.UUID(results[0])
        assert parsed.version == 5

    def test_md5_method_consistency(self):
        """Test that MD5 method generates consistent UUIDs."""
        input_text = "test input"
        results = []
        
        for _ in range(3):
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "md5"
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be identical
        assert len(set(results)) == 1
        # Should be valid UUID v3
        parsed = uuid.UUID(results[0])
        assert parsed.version == 3

    def test_truncate_method_consistency(self):
        """Test that truncate method generates consistent UUID-like strings."""
        input_text = "test input"
        results = []
        
        for _ in range(3):
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "truncate"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All results should be identical
        assert len(set(results)) == 1
        # Should be valid UUID format
        assert len(results[0]) == 36
        parts = results[0].split('-')
        assert len(parts) == 5

    def test_different_methods_different_results(self):
        """Test that different methods produce different results for same input."""
        input_text = "test input"
        results = {}
        
        for method in ["sha1", "md5", "truncate"]:
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = method
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results[method] = node.true_path
        
        # All methods should produce different results
        assert len(set(results.values())) == 3

    def test_different_namespaces_sha1(self):
        """Test that different namespaces produce different results for SHA-1."""
        input_text = "test input"
        results = []
        
        for namespace in ["DNS", "URL", "OID", "X500"]:
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "sha1"
            node.namespace = namespace
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All namespaces should produce different results
        assert len(set(results)) == 4

    def test_different_namespaces_md5(self):
        """Test that different namespaces produce different results for MD5."""
        input_text = "test input"
        results = []
        
        for namespace in ["DNS", "URL", "OID", "X500"]:
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "md5"
            node.namespace = namespace
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All namespaces should produce different results
        assert len(set(results)) == 4

    def test_truncate_ignores_namespace(self):
        """Test that truncate method ignores namespace parameter."""
        input_text = "test input"
        results = []
        
        for namespace in ["DNS", "URL", "OID", "X500"]:
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "truncate"
            node.namespace = namespace
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All should be the same (namespace ignored)
        assert len(set(results)) == 1

    def test_different_inputs_different_outputs(self):
        """Test that different inputs produce different outputs."""
        inputs = ["input1", "input2", "input3"]
        results = []
        
        for input_text in inputs:
            node = UUIDFromString()
            node.true_path = False
            node.false_path = False
            node.input_string = input_text
            node.method = "sha1"
            node.namespace = "DNS"
            asyncio.run(node.execute())
            results.append(node.true_path)
        
        # All should be different
        assert len(set(results)) == 3

    def test_empty_string_input(self):
        node = UUIDFromString()
        node.true_path = False
        node.false_path = False
        node.input_string = ""
        node.method = "sha1"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        # Should still generate a valid UUID
        assert isinstance(node.true_path, str)
        assert node.false_path is False
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 5

    def test_unicode_input(self):
        node = UUIDFromString()
        node.true_path = False
        node.false_path = False
        node.input_string = "héllo wörld 🚀"
        node.method = "sha1"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        # Should handle unicode correctly
        assert isinstance(node.true_path, str)
        assert node.false_path is False
        parsed = uuid.UUID(node.true_path)
        assert parsed.version == 5

    def test_non_string_input(self):
        node = UUIDFromString()
        node.true_path = False
        node.false_path = False
        node.input_string = 123
        node.method = "sha1"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Input must be a string" in str(node.false_path)

    def test_invalid_method(self):
        node = UUIDFromString()
        node.true_path = False
        node.false_path = False
        node.input_string = "test"
        node.method = "invalid"
        node.namespace = "DNS"
        asyncio.run(node.execute())
        
        assert node.true_path is False
        assert "Invalid method" in str(node.false_path)