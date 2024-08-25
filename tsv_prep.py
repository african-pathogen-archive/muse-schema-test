import csv
import json
import argparse

# CHECK

def read_tsv(file_path):
    with open(file_path, newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        return reader.fieldnames

def load_tsv_schema(schema_path):
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    return schema  # Returning the full schema (list of dicts)

def validate_headers(tsv_headers, schema):
    expected_headers = [field["name"] for field in schema]
    return set(tsv_headers) == set(expected_headers)

# FILL

def read_tsv_rows(file_path):
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
        json_data = json.loads(filled_template)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        raise
    
    # Add the additional "files" structure
    json_data["files"] = [
        {
            "fileName": "fakeName.fasta",
            "dataType": "FASTA",
            "fileType": "FASTA",
            "fileSize": 1000,
            "fileAccess": "open",
            "fileMd5sum": "fake"
        }
    ]
    
    return json_data

def validate_required_fields(row_data, schema):
    for field in schema:
        if field.get("requireNotEmpty", False):
            if not row_data.get(field["name"]):
                print(f"Row skipped due to missing required field: {field['name']}")
                return False
    return True

def main(tsv_file, schema_file, template_file=None, output_dir="."):
    tsv_headers = read_tsv(tsv_file)
    schema = load_tsv_schema(schema_file)

    if validate_headers(tsv_headers, schema):
        print("Headers match the schema!")
        print("Continuing to fill the template...")

        rows = read_tsv_rows(tsv_file)
        template_str = load_template(template_file)

        for i, row in enumerate(rows):
            if validate_required_fields(row, schema):
                filled_json = fill_template(template_str, row)
                output_path = f"{output_dir}/result_{i+1}.json"
                with open(output_path, 'w') as output_file:
                    json.dump(filled_json, output_file, indent=2)
                print(f"Generated: {output_path}")
            else:
                print(f"Row {i+1} skipped due to missing required fields.")

    else:
        print("Headers do not match the schema.")

        for header in [field["name"] for field in schema]:
            if header not in tsv_headers:
                print("Missing header in TSV:" + header)
        
        for header in tsv_headers:
            if header not in [field["name"] for field in schema]:
                print("Unexpected headers in TSV:" + header)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate TSV headers against a schema")
    
    # Required argument
    parser.add_argument("tsv_file", help="Path to the TSV file")
    
    # Optional arguments
    parser.add_argument("schema_file", help="Path to the TSV schema JSON file", nargs='?', default="tsv-schema.json")
    parser.add_argument("template_file", help="Path to the payload template JSON file", nargs='?', default="payload-template.json")
    parser.add_argument("output_dir", help="Directory to save the resulting JSON files", nargs='?', default=".")

    args = parser.parse_args()
    main(args.tsv_file, args.schema_file, args.template_file, args.output_dir)
