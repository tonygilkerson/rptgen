import argparse
import os
import sys
import yaml
import re

def remove_markdown_links(mod_file):
    """
    Reads the given file, replaces all Markdown links of the format [linkname](URL)
    with just the linkname, and writes the updated content back to the same file.
    """
    try:
        # Read the content of the file
        with open(mod_file, 'r') as file:
            content = file.read()
        
        # Replace Markdown links with just the link name
        updated_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        
        # Write the updated content back to the file
        with open(mod_file, 'w') as file:
            file.write(updated_content)
        
        print(f"Markdown links replaced in file: {mod_file}")
    except Exception as e:
        print(f"Error while processing file '{mod_file}': {e}", file=sys.stderr)
        sys.exit(1)

def apply_replacements(log_file, replacements) -> str:
    # Generate the output file name by prefixing "mod" to the log file name
    output_file = f"{os.path.splitext(log_file)[0]}(mod){os.path.splitext(log_file)[1]}"
    
    # Read the log file and apply replacements
    try:
        with open(log_file, 'r') as file:
            log_content = file.read()
        
        for key, value in replacements.items():
            log_content = log_content.replace(key, value)
        
        with open(output_file, 'w') as file:
            file.write(log_content)
        
        print(f"Replacements applied and saved to new log file: {output_file}")
        return output_file
    
    except Exception as e:
        print(f"Error while applying replacements: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Process detail logs to generate summary report.")
    parser.add_argument(
        '-s', '--samples', 
        action='append', 
        required=True, 
        help="Specify a sample report file. Use multiple -s flags for multiple files."
    )
    parser.add_argument(
        '-l', '--log', 
        required=True, 
        help="File containing the raw daily activity log"
    )
    parser.add_argument(
        '-r', '--replacements', 
        required=True, 
        help="Path to a YAML file containing search/replace values to be applied to the activity log file."
    )
    
    args = parser.parse_args()
    
    # Check if all sample files exist
    for sample_file in args.samples:
        if not os.path.isfile(sample_file):
            print(f"Error: Sample file '{sample_file}' does not exist.", file=sys.stderr)
            sys.exit(1)
    
    # Check if the log file exists
    if not os.path.isfile(args.log):
        print(f"Error: Log file '{args.log}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Check if the replacements file exists and load it
    if not os.path.isfile(args.replacements):
        print(f"Error: replacement file '{args.replacements}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.replacements, 'r') as replacements_file:
            search_n_replace_dict = yaml.safe_load(replacements_file)
            if not isinstance(search_n_replace_dict, dict):
                print(f"Error: replacements file '{args.replacements}' must contain a single dictionary.", file=sys.stderr)
                sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Failed to parse replacements file '{args.replacements}': {e}", file=sys.stderr)
        sys.exit(1)
    
    print("Sample report files:", args.samples)
    print("Daily activity log file:", args.log)
    print("Search and replace values from replacements file:", search_n_replace_dict)
    
    # Apply replacements to the log file and save to a new file
    logs_modified = apply_replacements(args.log, search_n_replace_dict)

    # Remove links 
    remove_markdown_links(logs_modified)

if __name__ == '__main__':
    main()