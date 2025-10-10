"""
Prompt Validator Module
Validates prompts against the defined schema
"""

import json
import sys
from jsonschema import validate, ValidationError, Draft7Validator
from pathlib import Path
from typing import Tuple, Dict, List, Optional


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
    
    def validate_prompt(self, prompt_data: Dict) -> Tuple[bool, Optional[str], List[str]]:
        """
        Validate a prompt against the schema
        
        Args:
            prompt_data: Dictionary containing prompt data
            
        Returns:
            tuple: (is_valid, error_message, warnings)
        """
        warnings = []
        
        try:
            validate(instance=prompt_data, schema=self.schema)
            
            # Additional validation checks
            if 'score' in prompt_data:
                score = prompt_data['score']
                if not any(score.values()):
                    warnings.append("Score object exists but all values are empty")
                    
            if 'models_tested' in prompt_data and 'responses' in prompt_data:
                models_in_responses = set(prompt_data['responses'].keys())
                models_tested = set(prompt_data['models_tested'])
                if models_in_responses != models_tested:
                    warnings.append(
                        f"Mismatch between models_tested and response keys: "
                        f"tested={models_tested}, responses={models_in_responses}"
                    )
            
            if 'variables' in prompt_data and 'prompt' in prompt_data:
                prompt_text = prompt_data['prompt']
                for var in prompt_data['variables']:
                    if f"{{{var}}}" not in prompt_text:
                        warnings.append(f"Variable '{var}' not found in prompt text")
            
            return True, None, warnings
            
        except ValidationError as e:
            return False, str(e), warnings
    
    def validate_prompt_file(self, file_path: str) -> Tuple[bool, Optional[str], List[str]]:
        """
        Validate a prompt file
        
        Args:
            file_path: Path to the JSON file containing prompt data
            
        Returns:
            tuple: (is_valid, error_message, warnings)
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                prompt_data = json.load(f)
            return self.validate_prompt(prompt_data)
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}", []
        except FileNotFoundError:
            return False, f"File not found: {file_path}", []
        except Exception as e:
            return False, f"Unexpected error: {str(e)}", []
    
    def validate_directory(self, directory_path: str) -> Dict[str, Tuple[bool, Optional[str], List[str]]]:
        """
        Validate all JSON files in a directory
        
        Args:
            directory_path: Path to directory containing prompt files
            
        Returns:
            dict: Mapping of file paths to validation results
        """
        results = {}
        directory = Path(directory_path)
        
        if not directory.exists():
            return results
            
        for json_file in directory.rglob("*.json"):
            results[str(json_file)] = self.validate_prompt_file(str(json_file))
            
        return results


if __name__ == "__main__":
    validator = PromptValidator()
    
    # If a file path is provided as argument, validate that file
    if len(sys.argv) > 1:
        target = sys.argv[1]
        target_path = Path(target)
        
        if target_path.is_file():
            # Validate single file
            is_valid, error, warnings = validator.validate_prompt_file(target)
            if is_valid:
                print(f"✅ {target} passed validation.")
                if warnings:
                    print(f"⚠️  Warnings:")
                    for warning in warnings:
                        print(f"   - {warning}")
            else:
                print(f"❌ Validation error in {target}:")
                print(f"   {error}")
                sys.exit(1)
                
        elif target_path.is_dir():
            # Validate directory
            results = validator.validate_directory(target)
            if not results:
                print(f"⚠️  No JSON files found in {target}")
                sys.exit(0)
                
            passed = sum(1 for r in results.values() if r[0])
            failed = len(results) - passed
            
            print(f"\n📊 Validation Results for {target}")
            print(f"   Total: {len(results)} | ✅ Passed: {passed} | ❌ Failed: {failed}\n")
            
            for file_path, (is_valid, error, warnings) in results.items():
                if is_valid:
                    print(f"✅ {Path(file_path).name}")
                    if warnings:
                        for warning in warnings:
                            print(f"   ⚠️  {warning}")
                else:
                    print(f"❌ {Path(file_path).name}")
                    print(f"   {error}")
            
            if failed > 0:
                sys.exit(1)
        else:
            print(f"❌ Invalid path: {target}")
            sys.exit(1)
    else:
        # Example usage
        example_prompt = {
            "id": "example-001",
            "title": "Example Prompt",
            "category": "education",
            "prompt": "This is an example prompt",
            "responses": {
                "gpt-4": "Example response"
            }
        }
        
        is_valid, error, warnings = validator.validate_prompt(example_prompt)
        if is_valid:
            print("✓ Prompt is valid")
            if warnings:
                print("⚠️  Warnings:")
                for warning in warnings:
                    print(f"   - {warning}")
        else:
            print(f"✗ Validation error: {error}")
