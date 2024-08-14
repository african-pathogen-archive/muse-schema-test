import csv
import json
import argparse

def read_tsv(file_path):
    with open(file_path, newline='') as tsvfile:
        reader = csv.DictReader(tsvfile, delimiter='\t')
        return reader.fieldnames

def load_tsv_schema(schema_path):
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    return [field["name"] for field in schema]  

def validate_headers(tsv_headers, expected_headers):
    return set(tsv_headers) == set(expected_headers)

def main(tsv_file, schema_file):
    tsv_headers = read_tsv(tsv_file)
    expected_headers = load_tsv_schema(schema_file)

    if validate_headers(tsv_headers, expected_headers):
        print("Headers match the schema!")
    else:
        print("Headers do not match the schema.")

        for header in expected_headers:
            if header not in tsv_headers:
                print("Missing header in TSV:" + header)
        
        for header in tsv_headers:
            if header not in expected_headers:
                print("Unexpected headers in TSV:" + header)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate TSV headers against a schema")
    parser.add_argument("tsv_file", help="Path to the TSV file")
    parser.add_argument("schema_file", help="Path to the TSV schema JSON file")

    args = parser.parse_args()
    main(args.tsv_file, args.schema_file)
