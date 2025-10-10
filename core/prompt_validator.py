"""
Prompt Validator Module
Validates prompts against the defined schema
"""

import json
from jsonschema import validate, ValidationError
from pathlib import Path


class PromptValidator:
    """Validates prompts against the prompt schema"""
    
    def __init__(self, schema_path=None):
        """
        Initialize the validator with a schema
        
        Args:
            schema_path: Path to the JSON schema file
        """
        if schema_path is None:
            schema_path = Path(__file__).parent / "prompt_schema.json"
        
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
    
    def validate_prompt(self, prompt_data):
        """
        Validate a prompt against the schema
        
        Args:
            prompt_data: Dictionary containing prompt data
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            validate(instance=prompt_data, schema=self.schema)
            return True, None
        except ValidationError as e:
            return False, str(e)
    
    def validate_prompt_file(self, file_path):
        """
        Validate a prompt file
        
        Args:
            file_path: Path to the JSON file containing prompt data
            
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            with open(file_path, 'r') as f:
                prompt_data = json.load(f)
            return self.validate_prompt(prompt_data)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
        except FileNotFoundError:
            return False, f"File not found: {file_path}"


if __name__ == "__main__":
    # Example usage
    validator = PromptValidator()
    
    example_prompt = {
        "id": "example-001",
        "title": "Example Prompt",
        "category": "education",
        "prompt": "This is an example prompt"
    }
    
    is_valid, error = validator.validate_prompt(example_prompt)
    if is_valid:
        print("✓ Prompt is valid")
    else:
        print(f"✗ Validation error: {error}")
