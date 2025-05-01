import argparse
import os
import sys
import yaml
import re

def unredact(content: str, replacements: dict) -> str:
    """
    Searches the content for the values in the replacements dictionary
    and replaces them with their corresponding keys.
    """
    for key, value in replacements.items():
        # Use re.sub for case-insensitive replacement of values with keys
        content = re.sub(re.escape(value), key, content, flags=re.IGNORECASE)
    return content

def remove_stuff(content) -> str:
    """
    Replaces all Markdown links of the format [linkname](URL) found in the content
    with just the linkname, and replace URLs with a dummy URL then returns the updated content
    """
    
    # Replace Markdown links with just the link name
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

    # Replace URLs with a dummy URL
    content = re.sub(r'http[s]?://[^\s]+', r'http://localhost/redacted', content)
    
    return content

def write_outfile(infile: str, content: str) -> None:
    # Name the outfile base on infile
    # For example, if infile = /path/foo.md then the outfile will be /path/foo(redacted).md
    output_file = f"{os.path.splitext(infile)[0]}(redacted){os.path.splitext(infile)[1]}"

    
    with open(output_file, 'w') as file:
        file.write(content)
    
def apply_replacements(infile: str, replacements: dict) -> str:
    """"
    Read input file and replace each key in replacements with its corresponding value, then return the text"
    """
    with open(infile, 'r') as file:
        detail_content = file.read()
    
    for key, value in replacements.items():
        # Use re.sub for case-insensitive replacement
        detail_content = re.sub(re.escape(key), value, detail_content, flags=re.IGNORECASE)

    return detail_content


def main():
    parser = argparse.ArgumentParser(description="Process detail logs to generate summary report.")
    parser.add_argument(
        'action', 
        choices=['redact', 'unredact'], 
        help="Specify the action to perform: 'redact' or 'unredact'."
    )
    parser.add_argument(
        '-s', '--samples', 
        action='append', 
        required=False, 
        help="Specify a sample report file. Use multiple -s flags for multiple files."
    )
    parser.add_argument(
        '-i', '--infile', 
        required=False, 
        help="Input file containing the raw daily activity content"
    )
    parser.add_argument(
        '-r', '--replacements', 
        required=False, 
        help="Path to a YAML file containing search/replace values to be applied to the activity log file."
    )
    parser.add_argument(
        '--msr_redacted', 
        required=False, 
        help="Path to the target report file that has been redacted."
    )
    args = parser.parse_args()
    
    # Check if all sample files exist
    if args.samples:
        for sample_file in args.samples:
            if not os.path.isfile(sample_file):
                print(f"Error: Sample file '{sample_file}' does not exist.", file=sys.stderr)
                sys.exit(1)
    
    # Check if the infile exists
    if args.infile:
        if not os.path.isfile(args.infile):
            print(f"Error: Log file '{args.infile}' does not exist.", file=sys.stderr)
            sys.exit(1)
    
    # Check if the replacements file exists and load it
    search_n_replace_dict = {}
    if args.replacements:
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

    # Check if the target report file exists
    if args.msr_redacted:
        if not os.path.isfile(args.msr_redacted):
            print(f"Error: Target report file '{args.msr_redacted}' does not exist.", file=sys.stderr)
            sys.exit(1)

    # Perform the specified action
    if args.action == 'redact':
        if not args.infile or not args.replacements:
            print("Error: Both --infile and --replacements are required for the 'redact' action.", file=sys.stderr)
            sys.exit(1)
        
        # Apply replacements to the infile and save to a new file
        content = apply_replacements(args.infile, search_n_replace_dict)

        # Remove links and stuff
        content = remove_stuff(content)

        # Write output file
        write_outfile(args.infile, content)

    elif args.action == 'unredact':
        if not args.msr_redacted or not args.replacements:
            print("Error: Both --msr_redacted and --replacements are required for the 'unredact' action.", file=sys.stderr)
            sys.exit(1)
        
        # Read the target report redacted file
        with open(args.msr_redacted, 'r') as file:
            redacted_content = file.read()
        
        # Perform unredaction
        unredacted_content = unredact(redacted_content, search_n_replace_dict)
        
        # Generate the output file name by replacing "redacted" with "unredacted"
        output_file = args.msr_redacted.replace("(redacted)", "(unredacted)")
        
        # Write the unredacted content to the new file
        with open(output_file, 'w') as file:
            file.write(unredacted_content)
        
        print(f"Unredacted content written to: {output_file}")
        
    print("Done.")

if __name__ == '__main__':
    main()