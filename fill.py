import csv
import json
import argparse

def read_tsv(file_path):
    with open(file_path, newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        return list(reader)

def load_template(template_path):
    with open(template_path) as template_file:
        return template_file.read()

def fill_template(template_str, row_data):
    filled_template = template_str
    for key, value in row_data.items():
        placeholder = f"${{{key}}}"
        if placeholder in filled_template:
            print(f"Replacing placeholder {placeholder} with {value}")
            filled_template = filled_template.replace(placeholder, json.dumps(value))
        else:
            print(f"Placeholder {placeholder} not found in the template.")
    
    # Debugging output before trying to load JSON
    print("Filled Template:")
    print(filled_template)
    
    try:
        return json.loads(filled_template)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        raise


def main(tsv_file, template_file, output_dir):
    rows = read_tsv(tsv_file)
    template_str = load_template(template_file)

    for i, row in enumerate(rows):
        filled_json = fill_template(template_str, row)
        output_path = f"{output_dir}/result_{i+1}.json"
        with open(output_path, 'w') as output_file:
            json.dump(filled_json, output_file, indent=2)
        print(f"Generated: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fill payload template with TSV data")
    parser.add_argument("tsv_file", help="Path to the TSV file")
    parser.add_argument("template_file", help="Path to the payload template JSON file")
    parser.add_argument("output_dir", help="Directory to save the resulting JSON files")

    args = parser.parse_args()
    main(args.tsv_file, args.template_file, args.output_dir)
