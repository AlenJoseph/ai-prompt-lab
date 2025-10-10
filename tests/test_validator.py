"""
Unit tests for the PromptValidator class
"""

import json
import pytest
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "core"))

from prompt_validator import PromptValidator


@pytest.fixture
def validator():
    """Create a validator instance"""
    return PromptValidator()


@pytest.fixture
def valid_prompt():
    """Return a valid prompt for testing"""
    return {
        "id": "test-001",
        "title": "Test Prompt",
        "category": "education",
        "prompt": "This is a test prompt",
        "responses": {
            "gpt-4": "Test response"
        }
    }


@pytest.fixture
def valid_prompt_with_variables():
    """Return a valid prompt with variables"""
    return {
        "id": "test-002",
        "title": "Test Prompt with Variables",
        "category": "coding",
        "goal": "Test goal",
        "prompt": "Explain {concept} in {language}",
        "variables": ["concept", "language"],
        "tags": ["test", "example"],
        "models_tested": ["gpt-4"],
        "responses": {
            "gpt-4": "Test response"
        },
        "score": {
            "clarity": 5,
            "accuracy": 4,
            "creativity": 3
        },
        "last_updated": "2025-10-10"
    }


class TestPromptValidator:
    """Test suite for PromptValidator"""
    
    def test_valid_prompt(self, validator, valid_prompt):
        """Test validation of a valid prompt"""
        is_valid, error, warnings = validator.validate_prompt(valid_prompt)
        assert is_valid is True
        assert error is None
    
    def test_missing_required_field(self, validator):
        """Test validation fails when required field is missing"""
        invalid_prompt = {
            "id": "test-003",
            "title": "Missing Response",
            "category": "education",
            "prompt": "Test"
        }
        is_valid, error, warnings = validator.validate_prompt(invalid_prompt)
        assert is_valid is False
        assert "responses" in error.lower() or "required" in error.lower()
    
    def test_invalid_category(self, validator, valid_prompt):
        """Test validation fails with invalid category"""
        valid_prompt["category"] = "invalid_category"
        is_valid, error, warnings = validator.validate_prompt(valid_prompt)
        assert is_valid is False
    
    def test_invalid_id_pattern(self, validator, valid_prompt):
        """Test validation fails with invalid ID pattern"""
        valid_prompt["id"] = "TEST_001"  # Uppercase and underscore not allowed
        is_valid, error, warnings = validator.validate_prompt(valid_prompt)
        assert is_valid is False
    
    def test_score_out_of_range(self, validator, valid_prompt):
        """Test validation fails when score is out of range"""
        valid_prompt["score"] = {
            "clarity": 10,  # Max is 5
            "accuracy": 3
        }
        is_valid, error, warnings = validator.validate_prompt(valid_prompt)
        assert is_valid is False
    
    def test_variable_mismatch_warning(self, validator):
        """Test warning when variable not found in prompt"""
        prompt = {
            "id": "test-004",
            "title": "Variable Mismatch",
            "category": "education",
            "prompt": "This prompt has no variables",
            "variables": ["concept"],  # Variable defined but not in prompt
            "responses": {"gpt-4": "response"}
        }
        is_valid, error, warnings = validator.validate_prompt(prompt)
        assert is_valid is True
        assert len(warnings) > 0
        assert "concept" in warnings[0]
    
    def test_model_response_mismatch_warning(self, validator):
        """Test warning when models_tested doesn't match responses"""
        prompt = {
            "id": "test-005",
            "title": "Model Mismatch",
            "category": "education",
            "prompt": "Test",
            "models_tested": ["gpt-4", "claude-3"],
            "responses": {"gpt-4": "response"}  # Missing claude-3
        }
        is_valid, error, warnings = validator.validate_prompt(prompt)
        assert is_valid is True
        assert len(warnings) > 0
    
    def test_valid_prompt_with_all_fields(self, validator, valid_prompt_with_variables):
        """Test validation of prompt with all optional fields"""
        is_valid, error, warnings = validator.validate_prompt(valid_prompt_with_variables)
        assert is_valid is True
        assert error is None


class TestFileValidation:
    """Test file-based validation"""
    
    def test_validate_nonexistent_file(self, validator):
        """Test validation of non-existent file"""
        is_valid, error, warnings = validator.validate_prompt_file("nonexistent.json")
        assert is_valid is False
        assert "not found" in error.lower()
    
    def test_validate_invalid_json(self, validator, tmp_path):
        """Test validation of invalid JSON file"""
        invalid_file = tmp_path / "invalid.json"
        invalid_file.write_text("{ invalid json }")
        
        is_valid, error, warnings = validator.validate_prompt_file(str(invalid_file))
        assert is_valid is False
        assert "json" in error.lower()


def test_schema_file_exists():
    """Test that the schema file exists"""
    schema_path = Path(__file__).parent.parent / "core" / "prompt_schema.json"
    assert schema_path.exists()
    
    # Verify it's valid JSON
    with open(schema_path) as f:
        schema = json.load(f)
    
    assert "$schema" in schema
    assert "properties" in schema
    assert "required" in schema


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
