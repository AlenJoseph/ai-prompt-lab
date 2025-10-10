#!/usr/bin/env python3
"""
AI Prompt Lab CLI
Command-line interface for managing prompts
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime
from prompt_validator import PromptValidator


class PromptCLI:
    def __init__(self):
        self.validator = PromptValidator()
        self.base_path = Path(__file__).parent.parent
        
    def create_prompt(self, args):
        """Interactive prompt creation wizard"""
        print("🧠 AI Prompt Lab - Create New Prompt\n")
        
        # Gather information
        prompt_id = input("Prompt ID (e.g., edu-001): ").strip()
        title = input("Title: ").strip()
        
        print("\nCategories: education, creative, productivity, coding")
        category = input("Category: ").strip()
        
        goal = input("Goal/Purpose: ").strip()
        prompt_text = input("Prompt text: ").strip()
        
        variables = input("Variables (comma-separated, or press Enter to skip): ").strip()
        variables_list = [v.strip() for v in variables.split(",")] if variables else []
        
        tags = input("Tags (comma-separated): ").strip()
        tags_list = [t.strip() for t in tags.split(",")]
        
        # Create prompt object
        prompt_data = {
            "id": prompt_id,
            "title": title,
            "category": category,
            "goal": goal,
            "prompt": prompt_text,
            "variables": variables_list,
            "tags": tags_list,
            "models_tested": [],
            "responses": {},
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Validate
        is_valid, error, warnings = self.validator.validate_prompt(prompt_data)
        
        if not is_valid:
            print(f"\n❌ Validation failed: {error}")
            return
        
        if warnings:
            print("\n⚠️  Warnings:")
            for warning in warnings:
                print(f"   - {warning}")
        
        # Save
        category_path = self.base_path / "prompts" / category
        category_path.mkdir(parents=True, exist_ok=True)
        
        filename = f"{prompt_id.replace('-', '_')}_{title.lower().replace(' ', '_')[:30]}.json"
        filepath = category_path / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(prompt_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Prompt created: {filepath}")
        print(f"\n💡 Next steps:")
        print(f"   1. Test with AI models")
        print(f"   2. Add responses to the JSON file")
        print(f"   3. Add scores after evaluation")
        
    def validate(self, args):
        """Validate prompts"""
        target = args.path if args.path else self.base_path / "prompts"
        
        if Path(target).is_file():
            is_valid, error, warnings = self.validator.validate_prompt_file(target)
            if is_valid:
                print(f"✅ {target} passed validation.")
                if warnings:
                    print("⚠️  Warnings:")
                    for warning in warnings:
                        print(f"   - {warning}")
            else:
                print(f"❌ {target} failed validation:")
                print(f"   {error}")
                sys.exit(1)
        else:
            results = self.validator.validate_directory(target)
            passed = sum(1 for r in results.values() if r[0])
            failed = len(results) - passed
            
            print(f"\n📊 Validation Results")
            print(f"   Total: {len(results)} | ✅ Passed: {passed} | ❌ Failed: {failed}\n")
            
            for filepath, (is_valid, error, warnings) in results.items():
                if is_valid:
                    print(f"✅ {Path(filepath).relative_to(self.base_path)}")
                else:
                    print(f"❌ {Path(filepath).relative_to(self.base_path)}")
                    print(f"   {error}")
            
            if failed > 0:
                sys.exit(1)
    
    def list_prompts(self, args):
        """List all prompts"""
        prompts_dir = self.base_path / "prompts"
        
        if args.category:
            category_path = prompts_dir / args.category
            if not category_path.exists():
                print(f"❌ Category '{args.category}' not found")
                return
            files = list(category_path.glob("*.json"))
        else:
            files = list(prompts_dir.rglob("*.json"))
        
        print(f"\n📚 Found {len(files)} prompts:\n")
        
        for filepath in sorted(files):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                category = data.get('category', 'unknown')
                title = data.get('title', 'Untitled')
                prompt_id = data.get('id', '?')
                print(f"  [{category:12}] {prompt_id:15} - {title}")
            except Exception as e:
                print(f"  ⚠️  Error reading {filepath.name}: {e}")
    
    def stats(self, args):
        """Show repository statistics"""
        prompts_dir = self.base_path / "prompts"
        results = self.validator.validate_directory(str(prompts_dir))
        
        categories = {}
        total_models = set()
        total_tags = set()
        
        for filepath, (is_valid, _, _) in results.items():
            if not is_valid:
                continue
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                cat = data.get('category', 'unknown')
                categories[cat] = categories.get(cat, 0) + 1
                
                if 'models_tested' in data:
                    total_models.update(data['models_tested'])
                
                if 'tags' in data:
                    total_tags.update(data['tags'])
                    
            except Exception:
                pass
        
        print("\n📊 AI Prompt Lab Statistics\n")
        print(f"Total Prompts: {len(results)}")
        print(f"Valid Prompts: {sum(1 for r in results.values() if r[0])}")
        print(f"\nBy Category:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat:15} {count:3}")
        print(f"\nUnique Models Tested: {len(total_models)}")
        if total_models:
            print(f"  {', '.join(sorted(total_models))}")
        print(f"\nUnique Tags: {len(total_tags)}")


def main():
    parser = argparse.ArgumentParser(
        description="AI Prompt Lab CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new prompt interactively')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate prompts')
    validate_parser.add_argument('path', nargs='?', help='File or directory to validate')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all prompts')
    list_parser.add_argument('-c', '--category', help='Filter by category')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show repository statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cli = PromptCLI()
    
    if args.command == 'create':
        cli.create_prompt(args)
    elif args.command == 'validate':
        cli.validate(args)
    elif args.command == 'list':
        cli.list_prompts(args)
    elif args.command == 'stats':
        cli.stats(args)


if __name__ == "__main__":
    main()
