import argparse
from pathlib import Path
from pipeline import AspectSentimentPipeline
from export import export_for_review

def analyze(args):
    input_file = args.input_file
    config = args.config
    output = args.output
    
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' does not exist")
        return
    if config and not Path(config).exists():
        print(f"Error: Config file '{config}' does not exist")
        return
    
    print(f"Analyzing {input_file} with config {config}, output to {output}")
    
    try:
        pipeline = AspectSentimentPipeline(config_file=config)
        
        input_path = Path(input_file).resolve()
        with open(input_path, 'r', encoding='utf-8') as fp:
            comments = [line.strip() for line in fp if line.strip()]
        
        if not comments:
            print("Warning: No comments found in input file")
            return
            
        print(f"Processing {len(comments)} comments...")
        
        results = pipeline.process_corpus(comments)
        export_for_review(results, output)
        
        print(f"Analysis complete. Results saved to {output}")
    
    except Exception as e:
        print(f"Error during analysis: {e}")
    
def main():
    parser = argparse.ArgumentParser(description='Aspect-based sentiment analysis tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    analyze_parser = subparsers.add_parser('analyze', help='Analyze aspects and sentiment in text data')
    analyze_parser.add_argument('input_file', help='Input file to analyze (one comment per line)')
    analyze_parser.add_argument('-c', '--config', required=True, help='Aspect config file (.yaml / .yml or .json)')
    analyze_parser.add_argument('-o', '--output', default='results.json', help='Output file (default: results.json)')
    analyze_parser.set_defaults(func=analyze)
    
    args = parser.parse_args()
    
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()