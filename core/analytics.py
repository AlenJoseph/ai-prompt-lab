"""
Prompt Analytics and Comparison Module
Analyze prompt performance and compare model responses
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict
import statistics


class PromptAnalytics:
    """Analyze and compare prompts"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = Path(prompts_dir)
        self.prompts = self._load_all_prompts()
    
    def _load_all_prompts(self) -> List[Dict]:
        """Load all valid prompts from directory"""
        prompts = []
        for json_file in self.prompts_dir.rglob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    prompts.append(json.load(f))
            except Exception:
                pass
        return prompts
    
    def get_category_stats(self) -> Dict:
        """Get statistics by category"""
        stats = defaultdict(lambda: {
            'count': 0,
            'avg_scores': defaultdict(list),
            'models_used': set()
        })
        
        for prompt in self.prompts:
            cat = prompt.get('category', 'unknown')
            stats[cat]['count'] += 1
            
            if 'score' in prompt:
                for metric, value in prompt['score'].items():
                    stats[cat]['avg_scores'][metric].append(value)
            
            if 'models_tested' in prompt:
                stats[cat]['models_used'].update(prompt['models_tested'])
        
        # Calculate averages
        result = {}
        for cat, data in stats.items():
            avg_scores = {
                metric: round(statistics.mean(values), 2) if values else 0
                for metric, values in data['avg_scores'].items()
            }
            result[cat] = {
                'count': data['count'],
                'avg_scores': avg_scores,
                'models_used': list(data['models_used'])
            }
        
        return result
    
    def compare_models(self, model1: str, model2: str) -> Dict:
        """Compare two models' performance"""
        comparison = {
            'model1': model1,
            'model2': model2,
            'prompts_tested': {
                'model1': 0,
                'model2': 0,
                'both': 0
            },
            'categories': defaultdict(lambda: {'model1': 0, 'model2': 0})
        }
        
        for prompt in self.prompts:
            models = prompt.get('models_tested', [])
            responses = prompt.get('responses', {})
            category = prompt.get('category', 'unknown')
            
            has_model1 = model1 in models or model1 in responses
            has_model2 = model2 in models or model2 in responses
            
            if has_model1:
                comparison['prompts_tested']['model1'] += 1
                comparison['categories'][category]['model1'] += 1
            if has_model2:
                comparison['prompts_tested']['model2'] += 1
                comparison['categories'][category]['model2'] += 1
            if has_model1 and has_model2:
                comparison['prompts_tested']['both'] += 1
        
        return comparison
    
    def get_top_prompts(self, metric: str = 'effectiveness', limit: int = 10) -> List[Dict]:
        """Get top-rated prompts by metric"""
        scored_prompts = []
        
        for prompt in self.prompts:
            if 'score' in prompt and metric in prompt['score']:
                scored_prompts.append({
                    'id': prompt.get('id'),
                    'title': prompt.get('title'),
                    'category': prompt.get('category'),
                    'score': prompt['score'][metric]
                })
        
        scored_prompts.sort(key=lambda x: x['score'], reverse=True)
        return scored_prompts[:limit]
    
    def get_coverage_report(self) -> Dict:
        """Generate test coverage report"""
        all_models = set()
        prompts_by_model = defaultdict(list)
        categories_by_model = defaultdict(set)
        
        for prompt in self.prompts:
            models = prompt.get('models_tested', [])
            all_models.update(models)
            
            for model in models:
                prompts_by_model[model].append(prompt.get('id'))
                categories_by_model[model].add(prompt.get('category'))
        
        coverage = {}
        for model in all_models:
            coverage[model] = {
                'total_prompts': len(prompts_by_model[model]),
                'categories_covered': len(categories_by_model[model]),
                'coverage_percentage': round(
                    len(prompts_by_model[model]) / len(self.prompts) * 100, 1
                ) if self.prompts else 0
            }
        
        return {
            'total_models': len(all_models),
            'models': coverage,
            'total_prompts': len(self.prompts)
        }
    
    def generate_report(self, output_file: Optional[str] = None) -> str:
        """Generate comprehensive analytics report"""
        report = []
        report.append("=" * 60)
        report.append("AI PROMPT LAB - ANALYTICS REPORT")
        report.append("=" * 60)
        report.append("")
        
        # Overall stats
        report.append(f"Total Prompts: {len(self.prompts)}")
        report.append("")
        
        # Category stats
        report.append("CATEGORY BREAKDOWN")
        report.append("-" * 60)
        cat_stats = self.get_category_stats()
        for cat, data in sorted(cat_stats.items()):
            report.append(f"\n{cat.upper()}")
            report.append(f"  Prompts: {data['count']}")
            if data['avg_scores']:
                report.append(f"  Average Scores:")
                for metric, score in data['avg_scores'].items():
                    report.append(f"    {metric}: {score}")
            report.append(f"  Models: {', '.join(data['models_used'])}")
        
        report.append("")
        
        # Coverage report
        report.append("MODEL COVERAGE")
        report.append("-" * 60)
        coverage = self.get_coverage_report()
        for model, data in sorted(coverage['models'].items()):
            report.append(f"\n{model}")
            report.append(f"  Prompts tested: {data['total_prompts']}")
            report.append(f"  Categories covered: {data['categories_covered']}")
            report.append(f"  Coverage: {data['coverage_percentage']}%")
        
        report.append("")
        report.append("=" * 60)
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
        
        return report_text


def main():
    """CLI for analytics module"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AI Prompt Lab Analytics")
    parser.add_argument('--report', action='store_true', help='Generate full report')
    parser.add_argument('--compare', nargs=2, metavar=('MODEL1', 'MODEL2'),
                       help='Compare two models')
    parser.add_argument('--top', type=int, default=10,
                       help='Show top N prompts')
    parser.add_argument('--metric', default='effectiveness',
                       help='Metric for top prompts')
    parser.add_argument('--output', help='Output file for report')
    
    args = parser.parse_args()
    
    analytics = PromptAnalytics()
    
    if args.report:
        report = analytics.generate_report(args.output)
        print(report)
    
    elif args.compare:
        comparison = analytics.compare_models(args.compare[0], args.compare[1])
        print(f"\nModel Comparison: {comparison['model1']} vs {comparison['model2']}")
        print(f"\nPrompts tested:")
        print(f"  {comparison['model1']}: {comparison['prompts_tested']['model1']}")
        print(f"  {comparison['model2']}: {comparison['prompts_tested']['model2']}")
        print(f"  Both: {comparison['prompts_tested']['both']}")
    
    else:
        top_prompts = analytics.get_top_prompts(args.metric, args.top)
        print(f"\nTop {args.top} Prompts by {args.metric}:")
        for i, prompt in enumerate(top_prompts, 1):
            print(f"  {i}. [{prompt['category']}] {prompt['title']} - Score: {prompt['score']}")


if __name__ == "__main__":
    main()
